import asyncio
import spacy
import json
import os
from spellchecker import SpellChecker
from typing import Callable, Optional, Dict, List
import uuid
from datetime import datetime
import re
import websockets
from fpdf import FPDF

class FluwdChatBot:
    def __init__(self, greeting: str, nlp_model: Optional[spacy.language.Language] = None):
        self.greeting = greeting
        self.nlp_model = nlp_model if nlp_model else spacy.load("en_core_web_sm")
        self.spell = SpellChecker()
        self.user_states = {}
        self.chat_history = []
        self.data_store_path = "chat_logs.json"
        self.load_chat_history()
    
    async def handle_chat(self, websocket, message_processor: Optional[Callable[[str], str]] = None):
        user_id = str(uuid.uuid4())
        await websocket.send(self.greeting)
        
        async for message in websocket:
            try:
                response = self.process_message(user_id, message)
                if not isinstance(response, str):
                    response = str(response)
                await websocket.send(response)
            except Exception as e:
                print(f"Error handling message: {e}")
                await websocket.send("An error occurred. Please try again.")
    
    def process_message(self, user_id: str, message: str) -> str:
        message = self.correct_spelling(message)
        intent = self.detect_intent(message)
        entities = self.extract_entities(message)
        response = self.rule_based_response(intent, entities)
        self.log_message(user_id, message, response)
        return response
    
    def correct_spelling(self, message: str) -> str:
        words = message.split()
        corrected_words = [self.spell.correction(word) if word else word for word in words]
        return " ".join(corrected_words)
    
    def detect_intent(self, message: str) -> str:
        message_lower = message.lower()
        if "hello" in message_lower:
            return "greeting"
        elif "generate project charter" in message_lower:
            return "generate_project_charter"
        elif "goodbye" in message_lower:
            return "farewell"
        return "unknown"
    
    def extract_entities(self, message: str) -> Dict[str, str]:
        doc = self.nlp_model(message)
        entities = {ent.label_: ent.text for ent in doc.ents}
        return entities
    
    def rule_based_response(self, intent: str, entities: Dict[str, str]) -> str:
        if intent == "greeting":
            return "Hello! How can I assist you today?"
        elif intent == "generate_project_charter":
            return self.generate_project_charter()
        elif intent == "farewell":
            return "Goodbye! Have a great day!"
        return "I'm not sure about that. Can you rephrase?"
    
    def log_message(self, user_id: str, message: str, response: str):
        timestamp = datetime.now().isoformat()
        entry = {"user_id": user_id, "timestamp": timestamp, "message": message, "response": response}
        self.chat_history.append(entry)
        with open(self.data_store_path, "w") as f:
            json.dump(self.chat_history, f, indent=4)
    
    def load_chat_history(self):
        if os.path.exists(self.data_store_path):
            with open(self.data_store_path, "r") as f:
                self.chat_history = json.load(f)
    
    def retrieve_last_project(self, user_id: str) -> Optional[Dict[str, str]]:
        for entry in reversed(self.chat_history):
            if entry["user_id"] == user_id and "project charter" in entry["response"].lower():
                return entry
        return None
    
    def search_chat_logs(self, keyword: str) -> List[Dict[str, str]]:
        return [entry for entry in self.chat_history if keyword.lower() in entry["message"].lower()]
    
    def generate_project_charter(self) -> str:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, "Project Charter", ln=True, align="C")
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, "Project Name: Sample Project\nObjectives: Define clear objectives and scope\nKey Details: Timeline, budget, and resources")
        pdf_file_path = "project_charter.pdf"
        pdf.output(pdf_file_path)
        return f"Project Charter has been generated and saved as {pdf_file_path}."
