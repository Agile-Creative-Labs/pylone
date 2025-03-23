import asyncio
import spacy
from spellchecker import SpellChecker
from typing import Callable, Optional, Dict, List
import uuid

class ChatHandler:
    def __init__(self, greeting: str, nlp_model: Optional[spacy.language.Language] = None):
        self.greeting = greeting
        self.nlp_model = nlp_model
        self.user_states = {}
        self.spell = SpellChecker()

    async def handle_chat(self, websocket, message_processor: Optional[Callable[[str], str]] = None):
        user_id = str(uuid.uuid4())
        await websocket.send(self.greeting)

        async for message in websocket:
            response = self.process_message(user_id, message)
            await websocket.send(response)

    def process_message(self, user_id: str, message: str) -> str:
        if "create project charter" in message.lower():
            self.user_states[user_id] = {"project_charter": {}, "current_step": "Project Name"}
            return "Great! Let's create a project charter. Please provide the project name."
        elif user_id in self.user_states:
            corrected_message = self.correct_input(message)
            if not self.is_valid_input(corrected_message):
                return "I'm sorry, I didn't understand that. Please provide a valid input."
            return self.collect_project_charter_info(user_id, corrected_message)
        else:
            return "I'm here to help you create a project charter. Just say 'create project charter' to get started!"

    def collect_project_charter_info(self, user_id: str, message: str) -> str:
        state = self.user_states[user_id]
        current_step = state["current_step"]

        if current_step == "Project Name":
            state["project_charter"]["Project Name"] = message
            state["current_step"] = "Objectives"
            return "Thank you! What are the objectives of the project?"
        elif current_step == "Objectives":
            state["project_charter"]["Objectives"] = message
            state["current_step"] = "Scope"
            return "Got it. What is the scope of the project?"
        elif current_step == "Scope":
            state["project_charter"]["Scope"] = message
            state["current_step"] = "Deliverables"
            return "Understood. What are the deliverables of the project?"
        elif current_step == "Deliverables":
            state["project_charter"]["Deliverables"] = message
            state["current_step"] = "Timeline"
            return "Noted. What is the timeline for the project?"
        elif current_step == "Timeline":
            state["project_charter"]["Timeline"] = message
            state["current_step"] = "Stakeholders"
            return "Almost done. Who are the stakeholders involved in the project?"
        elif current_step == "Stakeholders":
            state["project_charter"]["Stakeholders"] = message
            del self.user_states[user_id]
            return self.generate_project_charter(state["project_charter"])
        else:
            return "Something went wrong. Let's start over. Say 'create project charter' to begin."

    def generate_project_charter(self, project_charter: Dict[str, str]) -> str:
        charter = "\n".join(f"{key}: {value}" for key, value in project_charter.items())
        return f"Project Charter:\n{charter}"

    def is_valid_input(self, message: str) -> bool:
        # Spell checking
        words = message.split()
        unknown_words = self.spell.unknown(words)
        if len(unknown_words) / len(words) > 0.5:
            return False

        # Heuristic check
        if len(message) <= 5:
            return True  # Allow short inputs like acronyms or names
        if not self.heuristic_check(message):
            return False

        # NLP-based validation
        if self.nlp_model:
            doc = self.nlp_model(message)
            if not self.nlp_validation(doc):
                return False

        return True

    def heuristic_check(self, message: str) -> bool:
        # Simple heuristic: check for the presence of vowels or a minimum length
        vowels = set("aeiou")
        return any(char in vowels for char in message.lower()) or len(message) > 5

    def nlp_validation(self, doc) -> bool:
        # Check for the presence of nouns, verbs, proper nouns, or adjectives
        has_noun = any(token.pos_ == "NOUN" for token in doc)
        has_verb = any(token.pos_ == "VERB" for token in doc)
        has_proper_noun = any(token.pos_ == "PROPN" for token in doc)
        has_adjective = any(token.pos_ == "ADJ" for token in doc)
        return has_noun or has_verb or has_proper_noun or has_adjective

    def correct_input(self, message: str) -> str:
        words = message.split()
        corrected_words = []
        for word in words:
            if word in self.spell:
                corrected_words.append(self.spell.correction(word))
            else:
                corrected_words.append(word)
        corrected_message = ' '.join(corrected_words)
        if corrected_message.lower() != message.lower():
            return f"Did you mean: '{corrected_message}'? Please confirm or provide a corrected input."
        return corrected_message


