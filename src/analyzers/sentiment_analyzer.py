# Uses HuggingFace transformer model for sentiment if available
# Falls back gracefully if torch is not installed (e.g. on low memory servers)
try:
    from transformers import pipeline as hf_pipeline
    _sentiment_pipeline = hf_pipeline(
        "sentiment-analysis",
        model="cardiffnlp/twitter-roberta-base-sentiment",
        tokenizer="cardiffnlp/twitter-roberta-base-sentiment"
    )
    HF_AVAILABLE = True
except Exception:
    HF_AVAILABLE = False

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
    if not HF_AVAILABLE:
        # Return neutral placeholder if HF not available
        return {
            "hf_sentiment": "Unavailable",
            "hf_confidence": 0.0,
            "hf_sentiment_score": 0.0
        }

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