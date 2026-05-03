from flask import Flask, request, jsonify, render_template
from src.models.article import Article
from src.services.groq_client import analyze_article
from src.analyzers.scoring_service import compute_final_score
from src.utils.scraper import scrape_article

app = Flask(__name__)


@app.route("/")
def index():
    # Serve the main page
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()

    url = data.get("url", "").strip()
    text = data.get("text", "").strip()
    source = data.get("source", "Unknown")
    topic = data.get("topic", "General")

    # If URL provided, scrape it
    if url and not text:
        try:
            text = scrape_article(url)
        except Exception as e:
            return jsonify({"error": f"Could not scrape URL: {str(e)}"}), 400

    if not text:
        return jsonify({"error": "Please provide either a URL or article text"}), 400

    # Build article object
    article = Article(
        author="Unknown",
        url=url or "manual input",
        source_name=source,
        source_type="news",
        topic=topic,
        text=text,
        id="web-input"
    )

    try:
        ai_result = analyze_article(article)
        final_result = compute_final_score(article, ai_result)
    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

    # Clean up result for JSON serialization
    output = {
        "source": source,
        "topic": topic,
        "text_preview": text[:200] + "..." if len(text) > 200 else text,
        "bias_rating": final_result["bias_rating"],
        "bias_score": final_result["bias_score"],
        "sentiment": final_result["sentiment"],
        "sentiment_score": final_result["sentiment_score"],
        "misinformation_risk": final_result["misinformation_risk"],
        "misinformation_score": final_result["misinformation_score"],
        "blended_risk_score": final_result["blended_risk_score"],
        "loaded_language": final_result["loaded_language"],
        "flagged_words": final_result["distortion_analysis"]["loaded_words_found"],
        "key_issues": final_result["key_issues"],
        "summary": final_result["summary"],
        "hf_sentiment": final_result.get("hf_sentiment", "N/A"),
        "hf_confidence": final_result.get("hf_confidence", 0),
    }

    return jsonify(output)


if __name__ == "__main__":
    app.run(debug=True)