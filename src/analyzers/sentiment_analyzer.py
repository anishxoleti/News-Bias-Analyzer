# Uses a Hugging Face transformer model to classify sentiment
# This runs locally, no API call needed
from transformers import pipeline

# Load the model once at import time so we dont reload it on every article
# This model was trained on tweets so it handles informal language well
_sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment",
    tokenizer="cardiffnlp/twitter-roberta-base-sentiment"
)

LABEL_MAP = {
    "LABEL_0": "Negative",
    "LABEL_1": "Neutral",
    "LABEL_2": "Positive"
}

SCORE_MAP = {
    "Negative": -1.0,
    "Neutral": 0.0,
    "Positive": 1.0
}


def analyze_sentiment(text):
    # Truncate to 512 chars — transformer models have a token limit
    truncated = text[:512]

    result = _sentiment_pipeline(truncated)[0]

    label = LABEL_MAP.get(result["label"], "Neutral")
    confidence = round(result["score"], 3)
    numeric_score = round(SCORE_MAP[label] * confidence, 3)

    return {
        "hf_sentiment": label,
        "hf_confidence": confidence,
        "hf_sentiment_score": numeric_score
    }