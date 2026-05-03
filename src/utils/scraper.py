import requests
from bs4 import BeautifulSoup
from src.utils.text_cleaner import clean_text


def scrape_article(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove nav, footer, ads etc.
    for tag in soup(["script", "style", "nav", "footer", "aside", "header"]):
        tag.decompose()

    # Try to find the main article body
    article_tag = (
            soup.find("article") or
            soup.find("main") or
            soup.find("div", class_=lambda c: c and "article" in c.lower()) or
            soup.find("div", class_=lambda c: c and "content" in c.lower())
    )

    if article_tag:
        text = article_tag.get_text(separator=" ")
    else:
        # Fall back to all paragraph tags
        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text() for p in paragraphs)

    return clean_text(text)