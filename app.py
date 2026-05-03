from src.utils.json_loader import load_articles
from src.services.groq_client import analyze_article
from src.analyzers.scoring_service import compute_final_score
from src.analyzers.comparison_analyzer import compare_articles
from src.utils.result_saver import save_results


def print_result(article, result):
    print("\n" + "-" * 55)
    print(f"  Source: {article.source_name} ({article.source_type})")
    print(f"  Topic:  {article.topic}")
    print(f"  Text:   {article.text[:120]}{'...' if len(article.text) > 120 else ''}")
    print()
    print(f"  Bias:             {result['bias_rating']} (score: {result['bias_score']:+})")
    print(f"  Sentiment (AI):   {result['sentiment']} ({result['sentiment_score']:+.2f})")
    print(f"  Sentiment (HF):   {result['hf_sentiment']} (confidence: {result['hf_confidence']})")
    print(f"  Misinformation:   {result['misinformation_risk']} ({result['misinformation_score']}/10)")
    print(f"  Blended Risk:     {result['blended_risk_score']}/10 (AI + rule-based)")
    print(f"  Loaded Language:  {'Yes' if result['loaded_language'] else 'No'}")
    if result['distortion_analysis']['loaded_words_found']:
        print(f"  Flagged Words:    {', '.join(result['distortion_analysis']['loaded_words_found'])}")
    print(f"  Key Issues:       {', '.join(result['key_issues'])}")
    print()
    print(f"  Summary: {result['summary']}")
    print("-" * 55)

def print_comparison(comparison):
    print("\n" + "=" * 55)
    print("  COMPARISON REPORT")
    print("=" * 55)
    print(f"  Topic:               {comparison['topic']}")
    print(f"  Source A:            {comparison['source_a']}")
    print(f"  Source B:            {comparison['source_b']}")
    print(f"  Bias Divergence:     {comparison['bias_divergence']} / 10")
    print(f"  Sentiment Gap:       {comparison['sentiment_divergence']}")
    print(f"  Misinfo Gap:         {comparison['misinfo_divergence']} / 10")
    print(f"  Classification:      {comparison['classification']}")
    print("=" * 55)


if __name__ == "__main__":
    print("\nNews Bias & Misinformation Analyzer")
    print("Loading articles from sample_inputs.json...\n")

    articles = load_articles()
    print(f"Found {len(articles)} article(s). Analyzing...\n")

    results = []
    for article in articles:
        try:
            ai_result = analyze_article(article)
            final_result = compute_final_score(article, ai_result)
            results.append((article, final_result))
            print_result(article, final_result)
        except Exception as e:
            print(f"Error analyzing article {article.id}: {e}")

    # Compare articles on the same topic if we have pairs
    topics_seen = {}
    for article, result in results:
        if article.topic in topics_seen:
            prev_article, prev_result = topics_seen[article.topic]
            comparison = compare_articles(prev_article, prev_result, article, result)
            print_comparison(comparison)
        else:
            topics_seen[article.topic] = (article, result)

    # Save all results to a timestamped JSON file in results/
    save_results(results)

    print("\nDone.")