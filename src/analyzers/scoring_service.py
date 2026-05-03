# Combines AI output, Hugging Face sentiment, and our own distortion analysis
from src.analyzers.distortion_analyzer import analyze_distortion
from src.analyzers.sentiment_analyzer import analyze_sentiment


def compute_final_score(article, ai_result):
    # Run our own rule-based distortion check
    distortion = analyze_distortion(article.text)

    # Run Hugging Face sentiment model locally
    hf_result = analyze_sentiment(article.text)

    # Blend AI misinformation score with our distortion score
    ai_misinfo = ai_result.get("misinformation_score", 0)
    our_distortion = distortion["distortion_score"]

    # Weighted blend: 60% AI, 40% our own rule-based analysis
    blended_risk = round((ai_misinfo * 0.6) + (our_distortion * 0.4), 1)

    # Blend sentiment: 50% AI sentiment, 50% Hugging Face sentiment
    ai_sentiment_score = ai_result.get("sentiment_score", 0.0)
    hf_sentiment_score = hf_result["hf_sentiment_score"]
    blended_sentiment = round((ai_sentiment_score + hf_sentiment_score) / 2, 3)

    # Flag loaded language if either the AI or our analyzer caught it
    loaded_language = ai_result.get("loaded_language", False)
    if distortion["loaded_words_found"]:
        loaded_language = True

    return {
        **ai_result,
        "loaded_language": loaded_language,
        "sentiment_score": blended_sentiment,
        "hf_sentiment": hf_result["hf_sentiment"],
        "hf_confidence": hf_result["hf_confidence"],
        "distortion_analysis": distortion,
        "blended_risk_score": blended_risk
    }