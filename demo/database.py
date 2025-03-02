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

import sqlite3
from sqlite3 import Error
import logging
from demo.settings import config  # Import the loaded configuration

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class Database:
    def __init__(self):
        """Initialize the database connection and create tables."""
       # self.db_file = db_file
        self.db_file = config.DB_NAME
        self.conn = self.create_connection()
        self.create_table()

    def create_connection(self):
        """Create a database connection to the SQLite database."""
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            logging.debug("DemoDB Connection to SQLite DB successful")
        except Error as e:
            logging.error(f"DemoDB Error connecting to SQLite DB: {e}")
        return conn

    def create_table(self):
        """Create the users table if it doesn't exist."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                );
            """)
            self.conn.commit()
            logging.debug("DemoDB Users table created or already exists")
        except Error as e:
            logging.error(f"DemoDB Error creating users table: {e}")
    
    def add_user(self, username, password):
        """Add a new user to the database."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
            logging.debug(f"DemoDB User '{username}' added successfully")
            return True  # ✅ Return True if successful
        except Error as e:
            logging.error(f"DemoDB Error adding user: {e}")
            return False  # ✅ Return False if an error occurs


    def tadd_user(self, username, password):
        """Add a new user to the database."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
            logging.debug(f"DemoDB User '{username}' added successfully")
        except Error as e:
            logging.error(f"DemoDB Error adding user: {e}")
    
    def xadd_user(username, password):
        """Adds a user to the database."""
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
            conn.close()
            return True  # Return only one value
        except sqlite3.IntegrityError:
            conn.close()
            return False

    def get_user(self, username):
        """Retrieve a user from the database by username."""
        try:
            cursor = self.conn.cursor()
            logging.debug(f"DemoDB Executing query: SELECT * FROM users WHERE username = ?")
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            logging.debug(f"DemoDB Retrieved user: {user}")
            return user
        except Error as e:
            logging.error(f"DemoDB Error retrieving user: {e}")
            return None
    
    def get_user_by_id(self, user_id):
        """Retrieve a user from the database by user ID."""
        try:
            cursor = self.conn.cursor()
            logging.debug(f"DemoDB Executing query: SELECT * FROM users WHERE id = {user_id}")
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            user = cursor.fetchone()
            logging.debug(f"DemoDB Retrieved user: {user}")
            return user
        except Error as e:
            logging.error(f"DemoDB Error retrieving user: {e}")
            return None

    def get_all_users(self):
        """Retrieve all users from the database."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            logging.debug(f"DemoDB Retrieved {len(users)} users")
            return users
        except Error as e:
            logging.error(f"DemoDB Error retrieving users: {e}")
            return []

    def update_user(self, user_id, username, password):
        """Update a user in the database."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE users SET username = ?, password = ? WHERE id = ?", (username, password, user_id))
            self.conn.commit()
            logging.debug(f"DemoDB User {user_id} updated successfully")
        except Error as e:
            logging.error(f"DemoDB Error updating user: {e}")

    def delete_user(self, user_id):
        """Delete a user from the database."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            self.conn.commit()
            logging.debug(f"DemoDB User {user_id} deleted successfully")
        except Error as e:
            logging.error(f"DemoDB Error deleting user: {e}")

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            logging.debug("DemoDB Database connection closed")

# Initialize the database when this module is imported
db = Database()