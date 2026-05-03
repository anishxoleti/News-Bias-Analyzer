# News Bias & Misinformation Analyzer

A Python tool that analyzes news articles and social media posts for political bias,
sentiment, and misinformation risk using a combination of rule-based analysis and
a large language model via the Groq API.

## What it does

- Reads articles from a structured JSON dataset
- Cleans and preprocesses text before analysis
- Runs rule-based distortion detection (loaded language, emotional punctuation, caps ratio)
- Sends articles to an LLM for bias classification and sentiment scoring
- Blends both signals into a final risk score
- Compares articles on the same topic to measure narrative divergence
- Saves results to a timestamped JSON file in the results/ folder

## Project Structure