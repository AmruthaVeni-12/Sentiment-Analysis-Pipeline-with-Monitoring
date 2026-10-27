import pytest
import numpy as np
from src.models.svm_model import build_svm_pipeline

def test_svm_pipeline_training():
    # Supply at least 3 examples per class for 3-fold cross validation
    base_texts = [
        "Horrible, terrible, worst film ever made.",
        "Really bad and utterly disappointing.",
        "Average popcorn movie, nothing special.",
        "Good entertainment, solid acting and enjoyable.",
        "Masterpiece, brilliant and breathtaking!"
    ]
    texts = []
    labels = []
    for cls, txt in enumerate(base_texts):
        for rep in range(3):
            texts.append(f"{txt} repetition {rep}")
            labels.append(cls)

    pipeline = build_svm_pipeline(max_features=500, ngram_range=(1, 2), c_param=1.0, cv=3)
    pipeline.fit(texts, labels)

    preds = pipeline.predict(["Brilliant and breathtaking movie!"])
    assert len(preds) == 1
    assert preds[0] in [0, 1, 2, 3, 4]

    probs = pipeline.predict_proba(["Brilliant and breathtaking movie!"])
    assert probs.shape == (1, 5)
    # Probabilities must sum to ~1.0
    assert np.isclose(np.sum(probs), 1.0, atol=1e-4)
