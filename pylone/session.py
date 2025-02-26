import uuid
from datetime import datetime, timedelta

class Session:
    def __init__(self):
        self.sessions = {}  # Store sessions in memory

    def create_session(self, user_id):
        """Create a new session for a user."""
        session_id = str(uuid.uuid4())  # Generate a unique session ID
        expiry = datetime.now() + timedelta(hours=1)  # Set session expiry to 1 hour
        self.sessions[session_id] = {
            "user_id": user_id,
            "expiry": expiry
        }
        return session_id

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