import re
from typing import List, Dict, Any
from collections import Counter

# High-salience positive and negative lexicon for movie analysis
POSITIVE_KEYWORDS = {
    "masterpiece", "brilliant", "outstanding", "phenomenal", "exceptional",
    "captivating", "gripping", "terrific", "superb", "delightful", "entertaining",
    "charming", "smart", "refreshing", "satisfying", "compelling", "impressive",
    "engaging", "nuanced", "powerful", "flawless", "thrilling"
}

NEGATIVE_KEYWORDS = {
    "terrible", "horrible", "awful", "boring", "disappointing", "predictable",
    "atrocious", "cringeworthy", "unbearable", "torture", "lifeless", "shallow",
    "clumsy", "formulaic", "forgettable", "mess", "dull", "waste", "underwhelming",
    "incoherent", "poorly", "failed"
}

def extract_aspect_keywords(text: str) -> Dict[str, List[str]]:
    """Identifies mentioned positive and negative sentiment tokens in reviews."""
    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    pos_found = [w for w in words if w in POSITIVE_KEYWORDS]
    neg_found = [w for w in words if w in NEGATIVE_KEYWORDS]
    return {"pos": pos_found, "neg": neg_found}

def generate_rating_justification(
    movie_title: str,
    star_rating: float,
    sentiment_label: str,
    reviews: List[Dict[str, Any]],
    director: str = "",
    cast: str = ""
) -> str:
    """
    Generates a coherent 4 to 5 sentence justification explaining the calculated
    star rating based on aggregated user postings and extracted sentiment keywords.
    """
    if not reviews:
        return (
            f"'{movie_title}' currently has no registered user postings in the system. "
            f"Consequently, insufficient sentiment evidence exists to compute an audience-derived star rating. "
            f"Once audience critiques are submitted, our NLP engine will parse key sentiment drivers. "
            f"Please submit a review in Screen 2 to initialize sentiment aggregation."
        )

    total_reviews = len(reviews)
    all_text = " ".join([r.get("review_text", "") for r in reviews])
    aspects = extract_aspect_keywords(all_text)

    pos_counts = Counter(aspects["pos"])
    neg_counts = Counter(aspects["neg"])

    top_pos = [w for w, _ in pos_counts.most_common(3)]
    top_neg = [w for w, _ in neg_counts.most_common(3)]

    # Sentence 1: General consensus & overall star rating
    s1 = f"'{movie_title}' has earned an aggregated score of {star_rating:.1f} out of 5 stars based on {total_reviews} audience posting{'s' if total_reviews > 1 else ''}, placing it in the '{sentiment_label}' category."

    # Sentence 2: Narrative and plot consensus
    if star_rating >= 4.0:
        pos_str = f" emphasizing qualities like '{', '.join(top_pos)}'" if top_pos else ""
        s2 = f"Viewers overwhelmingly praised the storytelling and emotional resonance,{pos_str} which contributed to exceptionally high approval marks."
    elif star_rating >= 3.0:
        s2 = f"Audience feedback leans positively towards the central narrative and pacing, highlighting entertaining execution despite occasional minor pacing flaws."
    elif star_rating >= 2.5:
        s2 = f"Critiques reflect a divided consensus, with audiences finding the storyline serviceable and moderately engaging, though lacking groundbreaking originality."
    else:
        neg_str = f" repeatedly citing it as '{', '.join(top_neg)}'" if top_neg else ""
        s2 = f"A majority of reviews expressed strong disappointment with the narrative structure and dialogue,{neg_str} leading to depressed evaluation scores."

    # Sentence 3: Direction and cast execution
    personnel = []
    if director:
        personnel.append(f"direction by {director}")
    if cast:
        personnel.append(f"performances by {cast}")
    
    if personnel:
        personnel_phrase = " and ".join(personnel)
        if star_rating >= 3.5:
            s3 = f"The {personnel_phrase} was frequently singled out as a standout asset that elevated the cinematic experience."
        elif star_rating >= 2.5:
            s3 = f"Regarding creative execution, the {personnel_phrase} drew mixed reactions, delivering solid individual moments amidst inconsistent pacing."
        else:
            s3 = f"Additionally, the {personnel_phrase} struggled to overcome the limitations of the screenplay, failing to create genuine emotional investment."
    else:
        if star_rating >= 3.5:
            s3 = "Both the casting chemistry and directorial vision resonated strongly with the audience throughout the film's runtime."
        else:
            s3 = "Furthermore, key thematic moments were criticized for falling flat due to rushed character development and uneven direction."

    # Sentence 4: Key positive or critical takeaway
    if star_rating >= 4.0:
        s4 = "The cumulative analysis reveals an enthusiastic recommendation, particularly for fans of thoughtful, high-caliber drama and spectacle."
    elif star_rating >= 3.0:
        s4 = "Overall, the positive reception outweighs the critiques, establishing the film as an engaging and enjoyable viewing experience."
    elif star_rating >= 2.5:
        s4 = "The resulting rating underscores a balanced split where viewers appreciated specific scenes but remained neutral on the whole."
    else:
        s4 = "Ultimately, the preponderance of negative sentiment indicators and critical remarks explains the low rating assigned to this title."

    # Sentence 5: Concluding summary
    s5 = f"In summary, algorithmic feature extraction confirms that audience reaction firmly justifies the {star_rating:.1f}-star evaluation."

    return f"{s1} {s2} {s3} {s4} {s5}"
