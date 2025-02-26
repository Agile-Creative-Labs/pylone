import sqlite3
from sqlite3 import Error

# Database file path
DATABASE_FILE = "users.db"

def create_connection():
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"Error connecting to SQLite DB: {e}")
    return conn

def create_table(conn):
    """Create the users table if it doesn't exist."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            );
        """)
        conn.commit()
        print("Users table created or already exists")
    except Error as e:
        print(f"Error creating users table: {e}")

def initialize_database():
    """Initialize the database and create tables."""
    conn = create_connection()
    if conn:
        create_table(conn)
        conn.close()

def add_user(conn, username, password):
    """Add a new user to the database."""
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print(f"User '{username}' added successfully")
    except Error as e:
        print(f"Error adding user: {e}")

def get_user(conn, username):
    """Retrieve a user from the database by username."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return cursor.fetchone()
    except Error as e:
        print(f"Error retrieving user: {e}")
        return None

# Initialize the database when this module is imported
initialize_database()