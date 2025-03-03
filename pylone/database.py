"""pylone/database.py

This module provides a Database class for interacting with an SQLite database.
It handles database initialization, user registration, and user retrieval.

Key features:
    - Database initialization with a 'users' table.
    - User registration with unique username constraint.
    - User retrieval by username.
    - Generic query execution with fetchone and fetchall options.
    - Error handling and logging.

Usage:
    Initialize a Database instance:
    >>> db = Database()

    Register a user:
    >>> success = db.register_user("testuser", "password")

    Retrieve a user:
    >>> user = db.get_user("testuser")

    Execute a custom query:
    >>> results = db.execute("SELECT * FROM users", fetchall=True)
    Date Created: December 12, 2024
    Author: cooper@agilecreativelabs.ca
    Copyright: © 2025 Agile Creative Labs Inc.
"""
import sqlite3
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

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
        """Retrieve a user from the database by username."""
        try:
            return self.execute("SELECT * FROM users WHERE username = ?", (username,), fetchone=True)
        except sqlite3.Error as e:
            logging.error(f"Error retrieving user: {e}")
            return None

  