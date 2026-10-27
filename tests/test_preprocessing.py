import pytest
import pandas as pd
from src.data.preprocessing import clean_text, rating_to_class, prepare_dataframe, split_dataset

def test_clean_text():
    raw_html = "This movie was <b>fantastic</b>! &amp; deeply moving.<br /><br />Loved it."
    cleaned = clean_text(raw_html)
    assert "<b>" not in cleaned
    assert "<br />" not in cleaned
    assert "&amp;" not in cleaned
    assert "fantastic" in cleaned
    assert "Loved it." in cleaned

def test_rating_to_class():
    assert rating_to_class(1) == 0  # Very Negative
    assert rating_to_class(2) == 0
    assert rating_to_class(3) == 1  # Negative
    assert rating_to_class(4) == 1
    assert rating_to_class(5) == 2  # Neutral
    assert rating_to_class(6) == 2
    assert rating_to_class(7) == 3  # Positive
    assert rating_to_class(8) == 3
    assert rating_to_class(9) == 4  # Very Positive
    assert rating_to_class(10) == 4

def test_prepare_dataframe():
    df = pd.DataFrame({
        "review": ["Great movie!<br />", "Terrible film..."],
        "rating": [9, 2]
    })
    prepared = prepare_dataframe(df)
    assert "clean_review" in prepared.columns
    assert "sentiment_class" in prepared.columns
    assert "sentiment_label" in prepared.columns
    assert prepared.loc[0, "sentiment_class"] == 4
    assert prepared.loc[1, "sentiment_class"] == 0

def test_split_dataset():
    # Create sample balanced dataset
    data = []
    for cls in range(5):
        for i in range(20):
            data.append({"clean_review": f"review text {cls} {i}", "sentiment_class": cls})
    df = pd.DataFrame(data)

    train, val, test = split_dataset(df, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15)
    assert len(train) == 70
    assert len(val) == 15
    assert len(test) == 15
