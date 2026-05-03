# Combines AI output with our own distortion analysis into a final score
from src.analyzers.distortion_analyzer import analyze_distortion


def compute_final_score(article, ai_result):
    # Run our own rule-based distortion check on the raw text
    distortion = analyze_distortion(article.text)

    # Blend AI misinformation score with our distortion score
    ai_misinfo = ai_result.get("misinformation_score", 0)
    our_distortion = distortion["distortion_score"]

    # Weighted blend: 60% AI, 40% our own analysis
    blended_risk = round((ai_misinfo * 0.6) + (our_distortion * 0.4), 1)

    # Override loaded language flag if our analyzer caught something the AI missed
    loaded_language = ai_result.get("loaded_language", False)
    if distortion["loaded_words_found"]:
        loaded_language = True

    return {
        **ai_result,
        "loaded_language": loaded_language,
        "distortion_analysis": distortion,
        "blended_risk_score": blended_risk
    }