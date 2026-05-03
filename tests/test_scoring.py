# Basic tests for our own scoring logic - not testing the AI output
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.analyzers.distortion_analyzer import analyze_distortion
from src.analyzers.comparison_analyzer import compare_articles, classify_divergence


def test_loaded_language_detection():
    text = "This radical policy will destroy the economy and cause complete chaos!"
    result = analyze_distortion(text)
    assert len(result["loaded_words_found"]) > 0, "Should detect loaded words"
    assert result["distortion_score"] > 0, "Distortion score should be positive"
    print("  PASS: loaded language detection")


def test_clean_text_low_distortion():
    text = "Experts suggest the policy may have moderate effects on employment rates."
    result = analyze_distortion(text)
    assert result["distortion_score"] < 5, "Clean text should have low distortion"
    print("  PASS: clean text distortion")


def test_bias_divergence_classification():
    assert classify_divergence(1) == "Similar framing"
    assert classify_divergence(4) == "Moderate divergence"
    assert classify_divergence(8) == "High divergence - likely opposing narratives"
    print("  PASS: divergence classification")


def test_exclamation_detection():
    text = "This is outrageous!!! Nobody is safe!!!"
    result = analyze_distortion(text)
    assert result["exclamation_count"] == 6
    print("  PASS: exclamation detection")


if __name__ == "__main__":
    print("\nRunning tests...\n")
    test_loaded_language_detection()
    test_clean_text_low_distortion()
    test_bias_divergence_classification()
    test_exclamation_detection()
    print("\nAll tests passed.")