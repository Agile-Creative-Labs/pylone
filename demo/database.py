"""
Database Module for Demo Application.

This module provides a Database class that handles SQLite database operations
for the demo application. It initializes a database connection, creates the
users table if it doesn't exist, and provides methods for interacting with
the database.

Imports:
    sqlite3: For interacting with SQLite databases.
    sqlite3.Error: For handling SQLite database errors.
    logging: For logging messages.
    demo.settings.config: For accessing configuration settings, including the database name.

Classes:
    Database: Handles SQLite database operations.

Functions:
    None.

 Author: Agile Creative Labs Inc.
 Version: 1.0.0
 Date: 02/23/2024
 
"""
# demo/database.py
# demo/database.py
import sqlite3
from sqlite3 import Error
import logging
import threading
from demo.settings import config

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Thread-local storage
local = threading.local()

class Database:
    def __init__(self):
        """Initialize the database settings."""
        self.db_file = config.DB_NAME
        # Don't create a connection here!
        self.create_table()  # Create table if needed
    
    def get_connection(self):
        """Get a thread-local connection to the database."""
        if not hasattr(local, 'conn') or local.conn is None:
            try:
                local.conn = sqlite3.connect(self.db_file)
                logging.debug(f"Thread {threading.get_ident()}: New SQLite connection created")
            except Error as e:
                logging.error(f"Thread {threading.get_ident()}: Error connecting to SQLite DB: {e}")
        return local.conn

    def create_table(self):
        """Create the users table if it doesn't exist."""
        try:
            conn = self.get_connection()
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
    
    def add_user(self, username, password):
        """Add a new user to the database."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            logging.debug(f"User '{username}' added successfully")
            return True
        except Error as e:
            logging.error(f"Error adding user: {e}")
            return False

    def get_user(self, username):
        """Retrieve a user from the database by username."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            logging.debug(f"Executing query: SELECT * FROM users WHERE username = ?")
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            logging.debug(f"Retrieved user: {user}")
            return user
        except Error as e:
            logging.error(f"Error retrieving user: {e}")
            return None
    
    def get_user_by_id(self, user_id):
        """Retrieve a user from the database by user ID."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            logging.debug(f"Executing query: SELECT * FROM users WHERE id = {user_id}")
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            user = cursor.fetchone()
            logging.debug(f"Retrieved user: {user}")
            return user
        except Error as e:
            logging.error(f"Error retrieving user: {e}")
            return None

    def get_all_users(self):
        """Retrieve all users from the database."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            logging.debug(f"Retrieved {len(users)} users")
            return users
        except Error as e:
            logging.error(f"Error retrieving users: {e}")
            return []

    def update_user(self, user_id, username, password):
        """Update a user in the database."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET username = ?, password = ? WHERE id = ?", (username, password, user_id))
            conn.commit()
            logging.debug(f"User {user_id} updated successfully")
        except Error as e:
            logging.error(f"Error updating user: {e}")

    def delete_user(self, user_id):
        """Delete a user from the database."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            logging.debug(f"User {user_id} deleted successfully")
        except Error as e:
            logging.error(f"Error deleting user: {e}")

    def close(self):
        """Close the database connection for the current thread."""
        if hasattr(local, 'conn') and local.conn:
            local.conn.close()
            local.conn = None
            logging.debug(f"Thread {threading.get_ident()}: Database connection closed")

# Initialize the database when this module is imported
db = Database()