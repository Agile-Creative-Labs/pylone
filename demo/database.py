import logging
import sqlite3
from sqlite3 import Error

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Database file path
DATABASE_FILE = "users.db"

def create_connection():
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        logging.debug("Connection to SQLite DB successful")
    except Error as e:
        logging.error(f"Error connecting to SQLite DB: {e}")
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
        logging.debug("Users table created or already exists")
    except Error as e:
        logging.error(f"Error creating users table: {e}")

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
        logging.debug(f"User '{username}' added successfully")
    except Error as e:
        logging.error(f"Error adding user: {e}")

def get_user_by_id(conn, user_id):
    """Retrieve a user from the database by user ID."""
    try:
        cursor = conn.cursor()
        logging.debug(f"Executing query: SELECT * FROM users WHERE id = {user_id}")
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        logging.debug(f"Retrieved user: {user}")
        return user
    except Error as e:
        logging.error(f"Error retrieving user: {e}")
        return None

def get_user(conn, username):
    """Retrieve a user from the database by username."""
    try:
        cursor = conn.cursor()
        logging.debug(f"Executing query: SELECT * FROM users WHERE username = ?")
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))  # Pass username as a tuple
        user = cursor.fetchone()
        logging.debug(f"Retrieved user: {user}")
        return user
    except sqlite3.Error as e:
        logging.error(f"Error retrieving user: {e}")
        return None


def get_all_users(conn):
    """Retrieve all users from the database."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        logging.debug(f"Retrieved {len(users)} users")
        return users
    except Error as e:
        logging.error(f"Error retrieving users: {e}")
        return []

def update_user(conn, user_id, username, password):
    """Update a user in the database."""
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET username = ?, password = ? WHERE id = ?", (username, password, user_id))
        conn.commit()
        logging.debug(f"User {user_id} updated successfully")
    except Error as e:
        logging.error(f"Error updating user: {e}")

def delete_user(conn, user_id):
    """Delete a user from the database."""
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        logging.debug(f"User {user_id} deleted successfully")
    except Error as e:
        logging.error(f"Error deleting user: {e}")

# Initialize the database when this module is imported
initialize_database()