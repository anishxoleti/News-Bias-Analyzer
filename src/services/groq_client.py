import json
from groq import Groq
from src.config import GROQ_API_KEY, MODEL_NAME
from src.utils.prompt_builder import build_analysis_prompt
from src.utils.text_cleaner import clean_text

client = Groq(api_key=GROQ_API_KEY)


def analyze_article(article):
    # Clean the text before sending to AI
    article.text = clean_text(article.text)

    prompt = build_analysis_prompt(article)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
        temperature=0.3
    )

    raw = response.choices[0].message.content.strip()

    # Strip markdown code fences if the model adds them
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    return json.loads(raw)