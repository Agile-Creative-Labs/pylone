import uuid

class SessionManager:
    _sessions = {}

    @staticmethod
    def create_session(user_id):
        """Creates a session and returns session ID."""
        session_id = str(uuid.uuid4())
        SessionManager._sessions[session_id] = user_id
        return session_id

    @staticmethod
    def get_user(session_id):
        """Retrieves user ID from a session."""
        return SessionManager._sessions.get(session_id)
