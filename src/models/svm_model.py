import json
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Tuple
import matplotlib.pyplot as plt

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    classification_report,
    confusion_matrix
)
import mlflow
import mlflow.sklearn

from src.data.preprocessing import LABEL_MAP

MODELS_DIR = Path("models")
REPORTS_DIR = Path("reports")

def build_svm_pipeline(
    max_features: int = 25000,
    ngram_range: Tuple[int, int] = (1, 2),
    c_param: float = 1.0,
    cv: int = 3
) -> Pipeline:
    """Builds a TF-IDF + Calibrated LinearSVC pipeline."""
    base_svc = LinearSVC(
        C=c_param,
        loss="squared_hinge",
        penalty="l2",
        random_state=42,
        max_iter=3000
    )
    calibrated_svc = CalibratedClassifierCV(estimator=base_svc, method="sigmoid", cv=cv)

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            sublinear_tf=True,
            stop_words="english"
        )),
        ("classifier", calibrated_svc)
    ])
    return pipeline

def train_and_evaluate_svm(
    train_path: str = "data/processed/train.csv",
    val_path: str = "data/processed/val.csv",
    test_path: str = "data/processed/test.csv",
    experiment_name: str = "IMDb_5Class_Sentiment_Analysis"
) -> Dict[str, Any]:
    """Trains the SVM baseline, logs metrics/artifacts to MLflow, and saves the artifact."""
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # Load data
    train_df = pd.read_csv(train_path)
    val_df = pd.read_csv(val_path)
    test_df = pd.read_csv(test_path)

    X_train, y_train = train_df["clean_review"].fillna(""), train_df["sentiment_class"]
    X_val, y_val = val_df["clean_review"].fillna(""), val_df["sentiment_class"]
    X_test, y_test = test_df["clean_review"].fillna(""), test_df["sentiment_class"]

    # Set up MLflow with SQLite backend
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run(run_name="LinearSVC_Baseline") as run:
        # Params
        max_features = 25000
        ngram_range = (1, 2)
        c_param = 1.0

        mlflow.log_param("model_family", "SVM")
        mlflow.log_param("model_name", "LinearSVC_Calibrated")
        mlflow.log_param("max_features", max_features)
        mlflow.log_param("ngram_range", str(ngram_range))
        mlflow.log_param("C", c_param)
        mlflow.log_param("train_samples", len(X_train))

        # Train
        pipeline = build_svm_pipeline(max_features, ngram_range, c_param)
        pipeline.fit(X_train, y_train)

        # Validation & Test Predictions
        y_val_pred = pipeline.predict(X_val)
        y_test_pred = pipeline.predict(X_test)
        y_test_proba = pipeline.predict_proba(X_test)

        # Metrics
        val_acc = accuracy_score(y_val, y_val_pred)
        test_acc = accuracy_score(y_test, y_test_pred)
        macro_f1 = f1_score(y_test, y_test_pred, average="macro", zero_division=0)
        weighted_f1 = f1_score(y_test, y_test_pred, average="weighted", zero_division=0)
        precision = precision_score(y_test, y_test_pred, average="macro", zero_division=0)
        recall = recall_score(y_test, y_test_pred, average="macro", zero_division=0)

        mlflow.log_metric("val_accuracy", val_acc)
        mlflow.log_metric("test_accuracy", test_acc)
        mlflow.log_metric("test_macro_f1", macro_f1)
        mlflow.log_metric("test_weighted_f1", weighted_f1)
        mlflow.log_metric("test_macro_precision", precision)
        mlflow.log_metric("test_macro_recall", recall)

        # Confusion Matrix artifact
        cm = confusion_matrix(y_test, y_test_pred)
        fig, ax = plt.subplots(figsize=(8, 6))
        cax = ax.matshow(cm, cmap="Blues")
        fig.colorbar(cax)
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(j, i, str(cm[i, j]), va='center', ha='center', color='black')
        ax.set_xticks(range(5))
        ax.set_yticks(range(5))
        ax.set_xticklabels([LABEL_MAP[i] for i in range(5)], rotation=45, ha="left")
        ax.set_yticklabels([LABEL_MAP[i] for i in range(5)])
        plt.title("Confusion Matrix - Calibrated LinearSVC (5 Classes)", pad=20)
        plt.ylabel("True Sentiment")
        plt.xlabel("Predicted Sentiment")
        plt.tight_layout()
        cm_path = REPORTS_DIR / "svm_confusion_matrix.png"
        plt.savefig(cm_path)
        plt.close()
        mlflow.log_artifact(str(cm_path))

        # Classification Report artifact
        report = classification_report(
            y_test,
            y_test_pred,
            target_names=[LABEL_MAP[i] for i in range(5)],
            output_dict=True,
            zero_division=0
        )
        report_path = REPORTS_DIR / "svm_classification_report.json"
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)
        mlflow.log_artifact(str(report_path))

        # Save local model artifact
        local_model_path = MODELS_DIR / "svm_pipeline.joblib"
        joblib.dump(pipeline, local_model_path)

        # Log model to MLflow
        mlflow.sklearn.log_model(
            sk_model=pipeline,
            name="svm_model",
            serialization_format="cloudpickle",
            registered_model_name="MovieSentiment_SVM"
        )

        print(f"SVM Baseline Training Complete!")
        print(f" - Run ID: {run.info.run_id}")
        print(f" - Test Accuracy: {test_acc:.4f}")
        print(f" - Test Macro-F1: {macro_f1:.4f}")
        print(f" - Saved to: {local_model_path}")

        return {
            "run_id": run.info.run_id,
            "test_accuracy": test_acc,
            "test_macro_f1": macro_f1,
            "model_path": str(local_model_path)
        }

if __name__ == "__main__":
    train_and_evaluate_svm()
