import re


def strip_html(text):
    # Remove any HTML tags in case text was scraped from a webpage
    clean = re.sub(r'<[^>]+>', '', text)
    return clean


def normalize_whitespace(text):
    # Collapse multiple spaces/newlines into single space
    return re.sub(r'\s+', ' ', text).strip()


def normalize_quotes(text):
    # Replace curly/smart quotes with standard ones
    text = text.replace('\u2018', "'").replace('\u2019', "'")
    text = text.replace('\u201c', '"').replace('\u201d', '"')
    return text


def remove_urls(text):
    # Strip any embedded URLs from the text
    return re.sub(r'http\S+|www\.\S+', '', text)


def clean_text(text):
    # Run all cleaning steps in order
    text = strip_html(text)
    text = normalize_quotes(text)
    text = remove_urls(text)
    text = normalize_whitespace(text)
    return text