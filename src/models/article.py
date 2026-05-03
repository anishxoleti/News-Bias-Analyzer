#What info do I need to represent a single source
#I need author, name of article, url?, source name (Twitter, cnn),
# type (news article or tweet), topic, actual text
class Article:
    def __init__(self, author, url, source_name, source_type, topic, text, id):
        self.author = author
        self.url = url
        self.source_name = source_name
        self.source_type = source_type
        self.topic = topic
        self.text = text
        self.id = id
