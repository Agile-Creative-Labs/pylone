# pylone/chat_handler.py
import asyncio
import spacy
from textblob import TextBlob  # Simple sentiment analysis library
from typing import Callable, Optional

class ChatHandler:
    def __init__(self, greeting: str, nlp_model: Optional[spacy.language.Language] = None):
        self.greeting = greeting
        self.nlp_model = nlp_model

    async def handle_chat(self, websocket, message_processor: Optional[Callable[[str], str]] = None):
        await websocket.send(self.greeting)
        async for message in websocket:
            if self.nlp_model:
                doc = self.nlp_model(message)
                processed_message = self.process_with_nlp(doc)
            elif message_processor:
                processed_message = message_processor(message)
            else:
                processed_message = f"Echo: {message}"

            await websocket.send(processed_message)

    def process_with_nlp(self, doc):
        # Perform sentiment analysis
        sentiment = self.analyze_sentiment(doc.text)
        return f"Sentiment: {sentiment}. Processed Text: {' '.join([token.lemma_ for token in doc])}"

    def analyze_sentiment(self, text: str) -> str:
        # Use TextBlob for simple sentiment analysis
        analysis = TextBlob(text)
        if analysis.sentiment.polarity > 0:
            return "Positive"
        elif analysis.sentiment.polarity < 0:
            return "Negative"
        else:
            return "Neutral"