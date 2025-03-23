import spacy

class NLPWrapper:
    _instance = None  # Singleton instance for efficiency

    def __new__(cls, model="en_core_web_sm"):
        if cls._instance is None:
            cls._instance = super(NLPWrapper, cls).__new__(cls)
            cls._instance._load_model(model)
        return cls._instance

    def _load_model(self, model):
        """Load and cache the spaCy NLP model"""
        self.nlp = spacy.load(model)

    def process_text(self, text):
        """Process text and return the spaCy Doc object"""
        return self.nlp(text)

    def tokenize(self, text):
        """Return a list of tokens"""
        doc = self.process_text(text)
        return [token.text for token in doc]

    def named_entities(self, text):
        """Extract named entities (NER)"""
        doc = self.process_text(text)
        return [(ent.text, ent.label_) for ent in doc.ents]

    def pos_tags(self, text):
        """Return a list of words with their POS tags"""
        doc = self.process_text(text)
        return [(token.text, token.pos_) for token in doc]

    def dependency_parse(self, text):
        """Return dependency parsing information"""
        doc = self.process_text(text)
        return [(token.text, token.dep_, token.head.text) for token in doc]
