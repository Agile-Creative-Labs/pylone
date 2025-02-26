"""
    Session management system with functionalities for creating, retrieving, 
    validating, and deleting sessions, as well as handling CSRF tokens.
    Sessions are stored in memory and are set to expire after 1 hour.

    Date Created: February 26, 2025
    Author: alex@agilecreativelabs.ca
    Copyright: © 2025 Agile Creative Labs Inc.
"""
import uuid
from datetime import datetime, timedelta
import os
import binascii

class Session:
    def __init__(self):
        self.sessions = {}  # Store sessions in memory

    def create_session(self, user_id):
        """Create a new session for a user."""
        session_id = str(binascii.hexlify(os.urandom(16)).decode('utf-8'))  # Generate a unique session ID
        csrf_token = str(binascii.hexlify(os.urandom(16)).decode('utf-8'))  # Generate a CSRF token
        expiry = datetime.now() + timedelta(hours=1)  # Set session expiry to 1 hour
        self.sessions[session_id] = {
            "user_id": user_id,
            "csrf_token": csrf_token,
            "expiry": expiry
        }
        return session_id

    def get_csrf_token(self, session_id):
        """Retrieve the CSRF token for a session."""
        if session_id in self.sessions:
            return self.sessions[session_id]["csrf_token"]
        return None

    def validate_csrf_token(self, session_id, csrf_token):
        """Validate the CSRF token for a session."""
        if session_id in self.sessions:
            return self.sessions[session_id]["csrf_token"] == csrf_token
        return False

    def get_session(self, session_id):
        """Retrieve session data by session ID."""
        if session_id in self.sessions:
            session = self.sessions[session_id]
            if datetime.now() < session["expiry"]:  # Check if session is still valid
                return session
            else:
                del self.sessions[session_id]  # Delete expired session
        return None

    def delete_session(self, session_id):
        """Delete a session by session ID."""
        if session_id in self.sessions:
            del self.sessions[session_id]

# Create a global session manager
session_manager = Session()

