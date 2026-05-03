import json
from ..models.article import Article
#open and read JSON File
def load_articles():
    with open('data/sample_inputs.json','r', encoding = 'utf-8') as file:
        data = json.load(file)
    print(data)  #outputs parsed file as list of dictionaries

    #need to loop through data and create an Article object for each entry
    articles = []
    for x in data:
        author = x.get("author")
        url = x.get("url")
        source_name = x.get("source_name")
        source_type = x.get("source_type")
        topic = x.get("topic")
        text = x.get("text")
        id = x.get("id")

        article = Article(author, url, source_name, source_type, topic, text, id)
        articles.append(article)
    return articles