from groq import Groq
from src.config import GROQ_API_KEY, MODEL_NAME
from src.utils.prompt_builder import build_rewrite_prompt

client = Groq(api_key=GROQ_API_KEY)


def generate_neutral_rewrite(article, bias_rating):
    # Only bother rewriting if the article is actually biased
    if bias_rating in ("Center", "Center-Left", "Center-Right"):
        return None

    prompt = build_rewrite_prompt(article, bias_rating)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
        temperature=0.3
    )

    return response.choices[0].message.content.strip()