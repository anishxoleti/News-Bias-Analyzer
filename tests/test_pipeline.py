# Integration test - checks the full pipeline runs without crashing
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.models.article import Article
from src.analyzers.distortion_analyzer import analyze_distortion
from src.analyzers.comparison_analyzer import compare_articles
from src.analyzers.scoring_service import compute_final_score


def make_fake_ai_result(bias_score=0, sentiment_score=0.0, misinfo_score=2):
    # Fake AI result so we can test the pipeline without making real API calls
    return {
        "bias_rating": "Center",
        "bias_score": bias_score,
        "sentiment": "Neutral",
        "sentiment_score": sentiment_score,
        "misinformation_risk": "Low",
        "misinformation_score": misinfo_score,
        "loaded_language": False,
        "key_issues": ["economy", "jobs"],
        "summary": "A neutral take on the topic."
    }


def test_full_pipeline_runs():
    article = Article(
        author="Test Author",
        url="https://example.com",
        source_name="Test Source",
        source_type="news",
        topic="AI Regulation",
        text="Experts warn that AI could significantly affect jobs.",
        id="test-1"
    )

    ai_result = make_fake_ai_result()
    final = compute_final_score(article, ai_result)

    assert "blended_risk_score" in final, "Should have blended risk score"
    assert "distortion_analysis" in final, "Should have distortion analysis"
    print("  PASS: full pipeline runs")


def test_pipeline_catches_distortion():
    article = Article(
        author="Test Author",
        url="https://example.com",
        source_name="Tabloid",
        source_type="news",
        topic="Politics",
        text="This radical fraud will destroy everything! Total chaos and collapse!!!",
        id="test-2"
    )

    ai_result = make_fake_ai_result(misinfo_score=3)
    final = compute_final_score(article, ai_result)

    assert final["loaded_language"] == True, "Should flag loaded language"
    assert final["distortion_analysis"]["distortion_score"] > 0
    print("  PASS: pipeline catches distortion")


def test_pipeline_comparison():
    left_article = Article("A", "http://a.com", "Left News", "news", "Tax Policy", "This radical tax plan will destroy the middle class!", "l1")
    right_article = Article("B", "http://b.com", "Right News", "news", "Tax Policy", "The proposed tax reforms aim to stimulate economic growth.", "r1")

    left_ai = make_fake_ai_result(bias_score=-3, sentiment_score=-0.6, misinfo_score=4)
    right_ai = make_fake_ai_result(bias_score=3, sentiment_score=0.4, misinfo_score=2)

    left_final = compute_final_score(left_article, left_ai)
    right_final = compute_final_score(right_article, right_ai)

    comparison = compare_articles(left_article, left_final, right_article, right_final)

    assert comparison["bias_divergence"] == 6
    assert comparison["classification"] == "High divergence - likely opposing narratives"
    print("  PASS: comparison pipeline works")


if __name__ == "__main__":
    print("\nRunning pipeline tests...\n")
    test_full_pipeline_runs()
    test_pipeline_catches_distortion()
    test_pipeline_comparison()
    print("\nAll pipeline tests passed.")