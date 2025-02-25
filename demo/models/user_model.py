import sqlite3

class UserModel:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        """Initializes database with a users table."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            """)
            conn.commit()

    def register_user(self, username, password):
        """Registers a new user with a hashed password."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_user(self, username):
        """Retrieves user details by username."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            return cursor.fetchone()
