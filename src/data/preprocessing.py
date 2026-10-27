import re
import html
import pandas as pd
from typing import Tuple, Dict
from sklearn.model_selection import train_test_split

LABEL_MAP: Dict[int, str] = {
    0: "Very Negative",
    1: "Negative",
    2: "Neutral",
    3: "Positive",
    4: "Very Positive"
}

LABEL_STARS: Dict[int, int] = {
    0: 1,  # 1 star
    1: 2,  # 2 stars
    2: 3,  # 3 stars
    3: 4,  # 4 stars
    4: 5   # 5 stars
}

def clean_text(text: str) -> str:
    """Cleans movie review text by stripping HTML tags and normalizing whitespace."""
    if not isinstance(text, str):
        return ""
    # Unescape HTML entities (&quot;, &amp;, etc.)
    text = html.unescape(text)
    # Remove HTML tags (<br />, <p>, etc.)
    text = re.sub(r"<[^>]+>", " ", text)
    # Normalize multiple whitespace characters
    text = re.sub(r"\s+", " ", text).strip()
    return text

def rating_to_class(rating: int) -> int:
    """
    Converts 1-10 IMDb star rating to 5-class sentiment target:
    1-2  -> 0 (Very Negative)
    3-4  -> 1 (Negative)
    5-6  -> 2 (Neutral)
    7-8  -> 3 (Positive)
    9-10 -> 4 (Very Positive)
    """
    if rating <= 2:
        return 0
    elif rating <= 4:
        return 1
    elif rating <= 6:
        return 2
    elif rating <= 8:
        return 3
    else:
        return 4

def prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocesses a DataFrame containing 'review' and 'rating' columns."""
    df = df.copy()
    if "review" not in df.columns:
        raise ValueError("DataFrame must contain 'review' column")
    
    df["clean_review"] = df["review"].apply(clean_text)
    
    if "rating" in df.columns:
        df["sentiment_class"] = df["rating"].astype(int).apply(rating_to_class)
        df["sentiment_label"] = df["sentiment_class"].map(LABEL_MAP)
    elif "sentiment" in df.columns:
        # Fallback if binary sentiment is given (e.g. 'positive' / 'negative' or 1 / 0)
        # Map 0 -> Class 1 (Negative), 1 -> Class 3 (Positive) if raw binary
        if df["sentiment"].dtype == object:
            binary_map = {"negative": 1, "positive": 3}
            df["sentiment_class"] = df["sentiment"].str.lower().map(binary_map).fillna(2).astype(int)
        else:
            df["sentiment_class"] = df["sentiment"].apply(lambda s: 3 if s == 1 else 1)
        df["sentiment_label"] = df["sentiment_class"].map(LABEL_MAP)

    df["char_length"] = df["clean_review"].apply(len)
    df["word_count"] = df["clean_review"].apply(lambda t: len(t.split()))
    return df

def split_dataset(
    df: pd.DataFrame,
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Splits dataset with stratified sampling based on sentiment class."""
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-5, "Ratios must sum to 1.0"
    
    train_df, temp_df = train_test_split(
        df,
        test_size=(val_ratio + test_ratio),
        random_state=random_state,
        stratify=df["sentiment_class"]
    )
    
    relative_test_ratio = test_ratio / (val_ratio + test_ratio)
    val_df, test_df = train_test_split(
        temp_df,
        test_size=relative_test_ratio,
        random_state=random_state,
        stratify=temp_df["sentiment_class"]
    )
    
    return train_df.reset_index(drop=True), val_df.reset_index(drop=True), test_df.reset_index(drop=True)
