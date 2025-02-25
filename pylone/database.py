import sqlite3

class Database:
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

    def execute(self, query, params=(), fetchone=False, fetchall=False):
        """Executes a query and returns results if needed."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

            if fetchone:
                return cursor.fetchone()
            if fetchall:
                return cursor.fetchall()

    def register_user(self, username, password):
        """Registers a new user with a hashed password."""
        try:
            self.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            return True
        except sqlite3.IntegrityError:
            return False

    def get_user(self, username):
        """Retrieves user details by username."""
        return self.execute("SELECT * FROM users WHERE username = ?", (username,), fetchone=True)
