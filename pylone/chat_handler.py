import asyncio
import spacy
from spellchecker import SpellChecker
from typing import Callable, Optional, Dict, List
import uuid
from datetime import datetime
import re
import websockets


class ChatHandler:
    def __init__(
        self, greeting: str, nlp_model: Optional[spacy.language.Language] = None
    ):
        self.greeting = greeting
        self.nlp_model = nlp_model
        self.user_states = {}
        self.spell = SpellChecker()

    async def handle_chat(
        self, websocket, message_processor: Optional[Callable[[str], str]] = None
    ):
        user_id = str(uuid.uuid4())
        await websocket.send(self.greeting)  # Send the greeting message

        async for message in websocket:
            try:
                # Process the incoming message
                response = self.process_message(user_id, message)
                # Ensure the response is a string before sending
                if not isinstance(response, str):
                    response = str(response)
                await websocket.send(response)
            except Exception as e:
                print(f"Error handling message: {e}")
                await websocket.send("An error occurred. Please try again.")

    def process_message(self, user_id: str, message: str) -> str:
        if "create project charter" in message.lower():
            self.user_states[user_id] = {
                "project_charter": {},
                "current_step": "Project Name",
            }
            return "Great! Let's create a project charter. Please provide the project name."
        elif user_id in self.user_states:
            # Check if the message is a correction suggestion
            if message.startswith("Did you mean:"):
                # Extract the suggested correction
                match = re.search(r"'(.*?)'", message)
                if match:
                    message = match.group(1)
                
            corrected_message = self.check_spelling(message)
            if corrected_message.startswith("Did you mean:"):
                return corrected_message  # Return the suggestion to the user
            
            if not self.is_valid_input(corrected_message):
                return (
                    "I'm sorry, I didn't understand that. Please provide a valid input."
                )
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
            charter = self.generate_project_charter(state["project_charter"])
            del self.user_states[user_id]
            return charter
        else:
            return "Something went wrong. Let's start over. Say 'create project charter' to begin."

    def deprecated_generate_project_charter(
        self, project_charter: Dict[str, str]
    ) -> str:
        charter = "\n".join(f"{key}: {value}" for key, value in project_charter.items())
        return f"Project Charter:\n{charter}"

    def is_valid_input(self, message: str) -> bool:
        # Spell checking already done in check_spelling
        if not message or len(message) == 0:
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

    def check_spelling(self, message: str) -> str:
        """
        Check spelling but only return a suggestion, don't automatically correct.
        Returns the original message or a suggestion string.
        """
        words = message.split()
        if not words:
            return message
            
        unknown_words = self.spell.unknown(words)
        
        # If more than 50% of words are unknown, suggest corrections
        if len(unknown_words) > 0 and len(unknown_words) / len(words) > 0.5:
            corrected_words = []
            for word in words:
                if word not in self.spell:
                    corrected_words.append(self.spell.correction(word))
                else:
                    corrected_words.append(word)
            corrected_message = " ".join(corrected_words)
            
            if corrected_message.lower() != message.lower():
                return f"Did you mean: '{corrected_message}'? Please confirm or provide a corrected input."
        
        return message  # Return original message if no suggestion needed

    def generate_project_charter(self, user_inputs: Dict[str, str]) -> str:
        """
        Dynamically replaces placeholders in the template with user-provided inputs.

        Args:
            user_inputs (Dict[str, str]): A dictionary containing user-provided values for placeholders.

        Returns:
            str: A fully formatted project charter.
        """
        # Define the template
        template = """
**Project Charter: {Project Name}**

**1. Project Information**

* **Project Name:** {Project Name}
* **Project Manager:** (To be assigned)
* **Date Prepared:** {Date Prepared}

**2. Project Objectives**

* {Objectives}

**3. Project Scope**

* {Scope}

**4. Project Deliverables**

* {Deliverables}

**5. Timeline**

* {Timeline}

**6. Stakeholders**

* {Stakeholders}

**7. Assumptions**

* {Deliverables} can be procured and delivered within the {Timeline}.
* {Stakeholders} have the authority to make all necessary decisions.
* The {Scope} is a manageable scope within the {Timeline}.

**8. Constraints**

* **Time:** The project must be completed within {Timeline}.
* **Resources:** Limited resources are implied, given the short timeline.
* **Scope ambiguity:** The scope of "{Scope}" is extremely broad and will need immediate and strict scope management.
* The objectives of "{Objectives}" are extremely abstract.

**9. Risks**

* The abstract nature of the objectives may lead to difficulty in measuring success.
* The vast scope of "{Scope}" presents significant logistical and practical challenges.
* The short timeline of "{Timeline}" may lead to compromised quality.
* Lack of clear definition of "{Deliverables}" may lead to delays.

**10. Approval**

* (Signature) _________________________
* (Name) {Stakeholders}
* (Date) _________________________
"""

        # Automatically populate the "Date Prepared" field
        user_inputs["Date Prepared"] = datetime.now().strftime("%B %d, %Y")

        # Define the placeholder replacement function
        def placeholder_replacement(match):
            placeholder = match.group(1)  # Extract text inside {}
            return user_inputs.get(
                placeholder, f"[{placeholder} missing]"
            )  # Replace or flag missing placeholders

        # Replace placeholders dynamically
        formatted_charter = re.sub(r"\{(.*?)\}", placeholder_replacement, template)
        return formatted_charter