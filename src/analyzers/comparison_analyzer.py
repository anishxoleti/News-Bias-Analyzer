# Compares two articles on the same topic and computes divergence
# All math here is our own logic, no AI involved


def compute_bias_divergence(result_a, result_b):
    # How far apart are the two bias scores
    score_a = result_a.get("bias_score", 0)
    score_b = result_b.get("bias_score", 0)
    return abs(score_a - score_b)


def compute_sentiment_divergence(result_a, result_b):
    score_a = result_a.get("sentiment_score", 0.0)
    score_b = result_b.get("sentiment_score", 0.0)
    return round(abs(score_a - score_b), 2)


def compute_misinfo_divergence(result_a, result_b):
    score_a = result_a.get("misinformation_score", 0)
    score_b = result_b.get("misinformation_score", 0)
    return abs(score_a - score_b)


def classify_divergence(bias_div):
    # Classify how different the two articles are politically
    if bias_div <= 2:
        return "Similar framing"
    elif bias_div <= 5:
        return "Moderate divergence"
    else:
        return "High divergence - likely opposing narratives"


def compare_articles(article_a, result_a, article_b, result_b):
    bias_div = compute_bias_divergence(result_a, result_b)
    sentiment_div = compute_sentiment_divergence(result_a, result_b)
    misinfo_div = compute_misinfo_divergence(result_a, result_b)

    return {
        "source_a": article_a.source_name,
        "source_b": article_b.source_name,
        "topic": article_a.topic,
        "bias_divergence": bias_div,
        "sentiment_divergence": sentiment_div,
        "misinfo_divergence": misinfo_div,
        "classification": classify_divergence(bias_div)
    }