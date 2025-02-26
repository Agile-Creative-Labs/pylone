import sqlite3
from sqlite3 import Error
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def create_connection(db_file):
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        logging.debug("Connection to SQLite DB successful")
    except Error as e:
        logging.error(f"Error connecting to SQLite DB: {e}")
    return conn

def create_table(conn, table_sql):
    """Create a table in the database."""
    try:
        cursor = conn.cursor()
        cursor.execute(table_sql)
        conn.commit()
        logging.debug("Table created or already exists")
    except Error as e:
        logging.error(f"Error creating table: {e}")