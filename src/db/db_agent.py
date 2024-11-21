import logging
import sqlite3
import os

class DB_Agent:  # Database agent
    def __init__(self, db_name):
        self.db_name = os.path.abspath(db_name)  # Path to the database file (or name)
        self.conn = None  # Connection to the database
        self.cursor = None  # Cursor for executing SQL commands

        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)  # Configure logging


    def __del__(self):  # Destructor, make sure to close the connection once the object is deleted
        if self.conn:
            self.conn.close()


    def connect(self):
        """Connect to the SQLite database."""
        try:
            db_dir = os.path.dirname(self.db_name)  # Get the directory of the database file
            if db_dir and not os.path.exists(db_dir):  # Check if the folder exists
                os.makedirs(db_dir)  # Create the folder

            self.conn = sqlite3.connect(self.db_name)  # Connect to the database
            self.cursor = self.conn.cursor()  # Create a cursor object
            self.logger.info("Connected to the database successfully.")
        except Exception as e:  # Catch any exception that occurred during the connection and log it
            self.logger.error(f"Error connecting to the database: {e}")


    def disconnect(self):
        """Disconnect from the SQLite database."""
        if self.conn:  # Check if there is a connection to the database
            self.conn.close()  # Close the connection
            self.logger.info("Disconnected from the database successfully.")
            self.conn = None  # Reset the connection and cursor objects
            self.cursor = None  
        else:
            self.logger.warning("No connection to the database.")


    def initialize_db(self, schema_path):
        """Create the database schema."""
        self.connect()  # Connect to the database
        try:
            # Read the schema from the provided file
            with open(schema_path, 'r') as f:
                schema = f.read()  # Read the SQL commands from the file

            self.cursor.executescript(schema)  # Execute the SQL commands
            self.conn.commit()  # Commit the changes
            self.logger.info("Database schema created successfully.")
        except Exception as e:  
            self.logger.error(f"Error creating the database schema: {e}")
            if self.conn:
                self.conn.rollback()  # Rollback any changes if an error occurred
        finally:
            self.disconnect()  # Always disconnect after use


    def nuke_db(self):  # WARNING: Use this only as DEBUG during development
        """Completely remove the database and all of the data."""
        self.disconnect()  # Make sure the connection is severed
        try:
            os.remove(self.db_name)  # Delete the database file
            self.logger.info("Database nuked successfully.")
        except Exception as e:
            self.logger.error(f"Error nuking the database: {e}")
