import os
import json
import torch
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, List
import matplotlib.pyplot as plt

from torch.utils.data import Dataset, DataLoader
from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification,
    get_linear_schedule_with_warmup
)
from torch.optim import AdamW
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    classification_report,
    confusion_matrix
)
import mlflow
import mlflow.pytorch

from src.data.preprocessing import LABEL_MAP

MODELS_DIR = Path("models")
REPORTS_DIR = Path("reports")

class IMDbDataset(Dataset):
    """PyTorch Dataset for tokenized IMDb reviews."""
    def __init__(self, texts: List[str], labels: List[int], tokenizer, max_length: int = 128):
        self.encodings = tokenizer(
            texts,
            truncation=True,
            padding="max_length",
            max_length=max_length,
            return_tensors="pt"
        )
        self.labels = torch.tensor(labels, dtype=torch.long)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        item = {key: val[idx] for key, val in self.encodings.items()}
        item["labels"] = self.labels[idx]
        return item

def train_and_evaluate_distilbert(
    train_path: str = "data/processed/train.csv",
    val_path: str = "data/processed/val.csv",
    test_path: str = "data/processed/test.csv",
    epochs: int = 2,
    batch_size: int = 16,
    learning_rate: float = 2e-5,
    max_length: int = 128,
    experiment_name: str = "IMDb_5Class_Sentiment_Analysis"
) -> Dict[str, Any]:
    """Fine-tunes DistilBERT with FP16 support and logs parameters, metrics & artifacts to MLflow."""
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    use_fp16 = torch.cuda.is_available()
    print(f"DistilBERT Training on: {device} (FP16: {use_fp16})")

    # Load splits
    train_df = pd.read_csv(train_path)
    val_df = pd.read_csv(val_path)
    test_df = pd.read_csv(test_path)

    # Tokenizer & Datasets
    model_name = "distilbert-base-uncased"
    tokenizer = DistilBertTokenizerFast.from_pretrained(model_name)

    train_dataset = IMDbDataset(train_df["clean_review"].fillna("").tolist(), train_df["sentiment_class"].tolist(), tokenizer, max_length)
    val_dataset = IMDbDataset(val_df["clean_review"].fillna("").tolist(), val_df["sentiment_class"].tolist(), tokenizer, max_length)
    test_dataset = IMDbDataset(test_df["clean_review"].fillna("").tolist(), test_df["sentiment_class"].tolist(), tokenizer, max_length)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=0)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=0)

    # Model
    model = DistilBertForSequenceClassification.from_pretrained(model_name, num_labels=5)
    model.to(device)

    optimizer = AdamW(model.parameters(), lr=learning_rate, weight_decay=0.01)
    total_steps = len(train_loader) * epochs
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=int(total_steps * 0.1), num_training_steps=total_steps)
    scaler = torch.cuda.amp.GradScaler(enabled=use_fp16)

    # MLflow
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run(run_name="DistilBERT_FineTuned") as run:
        mlflow.log_param("model_family", "Transformer")
        mlflow.log_param("model_name", model_name)
        mlflow.log_param("epochs", epochs)
        mlflow.log_param("batch_size", batch_size)
        mlflow.log_param("learning_rate", learning_rate)
        mlflow.log_param("max_length", max_length)
        mlflow.log_param("fp16", use_fp16)
        mlflow.log_param("device", str(device))

        for epoch in range(epochs):
            model.train()
            total_train_loss = 0.0

            for batch in train_loader:
                optimizer.zero_grad()
                input_ids = batch["input_ids"].to(device)
                attention_mask = batch["attention_mask"].to(device)
                labels = batch["labels"].to(device)

                with torch.cuda.amp.autocast(enabled=use_fp16):
                    outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
                    loss = outputs.loss

                scaler.scale(loss).backward()
                scaler.step(optimizer)
                scaler.update()
                scheduler.step()

                total_train_loss += loss.item()

            avg_train_loss = total_train_loss / len(train_loader)
            mlflow.log_metric("train_loss", avg_train_loss, step=epoch + 1)

            # Validation evaluation
            model.eval()
            val_loss = 0.0
            val_preds, val_targets = [], []

            with torch.no_grad():
                for batch in val_loader:
                    input_ids = batch["input_ids"].to(device)
                    attention_mask = batch["attention_mask"].to(device)
                    labels = batch["labels"].to(device)

                    with torch.cuda.amp.autocast(enabled=use_fp16):
                        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
                    val_loss += outputs.loss.item()
                    preds = torch.argmax(outputs.logits, dim=1).cpu().numpy()
                    val_preds.extend(preds)
                    val_targets.extend(labels.cpu().numpy())

            val_acc = accuracy_score(val_targets, val_preds)
            mlflow.log_metric("val_loss", val_loss / len(val_loader), step=epoch + 1)
            mlflow.log_metric("val_accuracy", val_acc, step=epoch + 1)
            print(f"Epoch {epoch + 1}/{epochs} - Train Loss: {avg_train_loss:.4f} - Val Acc: {val_acc:.4f}")

        # Test set evaluation
        model.eval()
        test_preds, test_targets = [], []
        with torch.no_grad():
            for batch in test_loader:
                input_ids = batch["input_ids"].to(device)
                attention_mask = batch["attention_mask"].to(device)
                labels = batch["labels"].to(device)
                with torch.cuda.amp.autocast(enabled=use_fp16):
                    outputs = model(input_ids=input_ids, attention_mask=attention_mask)
                preds = torch.argmax(outputs.logits, dim=1).cpu().numpy()
                test_preds.extend(preds)
                test_targets.extend(labels.cpu().numpy())

        test_acc = accuracy_score(test_targets, test_preds)
        test_f1 = f1_score(test_targets, test_preds, average="macro", zero_division=0)
        mlflow.log_metric("test_accuracy", test_acc)
        mlflow.log_metric("test_macro_f1", test_f1)

        # Confusion Matrix artifact
        cm = confusion_matrix(test_targets, test_preds)
        fig, ax = plt.subplots(figsize=(8, 6))
        cax = ax.matshow(cm, cmap="Greens")
        fig.colorbar(cax)
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(j, i, str(cm[i, j]), va='center', ha='center', color='black')
        ax.set_xticks(range(5))
        ax.set_yticks(range(5))
        ax.set_xticklabels([LABEL_MAP[i] for i in range(5)], rotation=45, ha="left")
        ax.set_yticklabels([LABEL_MAP[i] for i in range(5)])
        plt.title("Confusion Matrix - DistilBERT (5 Classes)", pad=20)
        plt.ylabel("True Sentiment")
        plt.xlabel("Predicted Sentiment")
        plt.tight_layout()
        cm_path = REPORTS_DIR / "distilbert_confusion_matrix.png"
        plt.savefig(cm_path)
        plt.close()
        mlflow.log_artifact(str(cm_path))

        # Save local weights & tokenizer
        local_dir = MODELS_DIR / "distilbert_sentiment"
        local_dir.mkdir(parents=True, exist_ok=True)
        model.save_pretrained(local_dir)
        tokenizer.save_pretrained(local_dir)

        # Log to MLflow
        mlflow.pytorch.log_model(
            pytorch_model=model,
            artifact_path="distilbert_model",
            registered_model_name="MovieSentiment_DistilBERT"
        )

        print(f"DistilBERT Training Complete! Test Acc: {test_acc:.4f}, Macro-F1: {test_f1:.4f}")
        return {
            "run_id": run.info.run_id,
            "test_accuracy": test_acc,
            "test_macro_f1": test_f1,
            "model_path": str(local_dir)
        }

if __name__ == "__main__":
    train_and_evaluate_distilbert()
