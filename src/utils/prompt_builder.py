# Builds the prompt string sent to the AI
# Keeping this separate from the client makes it easy to tweak prompts without touching API logic


def build_analysis_prompt(article):
    return f"""
You are a media bias and misinformation detection system.

Analyze the following article and return ONLY a JSON object with no extra text or markdown.

Article Info:
- Source: {article.source_name} ({article.source_type})
- Topic: {article.topic}
- Author: {article.author}
- Text: {article.text}

Return this exact JSON structure:
{{
  "bias_rating": "<one of: Far-Left, Left, Center-Left, Center, Center-Right, Right, Far-Right>",
  "bias_score": <integer from -5 (far left) to 5 (far right)>,
  "sentiment": "<one of: Very Negative, Negative, Neutral, Positive, Very Positive>",
  "sentiment_score": <float from -1.0 to 1.0>,
  "misinformation_risk": "<one of: Low, Medium, High>",
  "misinformation_score": <integer from 0 to 10>,
  "loaded_language": <true or false>,
  "key_issues": ["<issue1>", "<issue2>"],
  "summary": "<one sentence explaining the rating>"
}}
"""


def build_rewrite_prompt(article, bias_rating):
    return f"""
The following article has been classified as {bias_rating}.

Rewrite it in a neutral, factual tone. Keep the same core information but remove
loaded language, emotional framing, and one-sided phrasing. Do not add new facts.

Original:
{article.text}

Return only the rewritten article text, nothing else.
"""