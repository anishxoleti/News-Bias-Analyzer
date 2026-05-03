#after I analyze one article, what info do I want to store?
#key terms?, tone of the article?
class Analysis:
    def __init__(self, tone_score, exaggeration_score, certainty_score, objectivity_score,
                 missing_context_score, flagged_phrases, explanation, article_id):
        self.tone_score = tone_score
        self.exaggeration_score = exaggeration_score
        self.certainty_score = certainty_score
        self.objectivity_score = objectivity_score
        self.missing_context_score = missing_context_score
        self.flagged_phrases = flagged_phrases
        self.explanation = explanation
        self.article_id = article_id
