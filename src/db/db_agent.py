"""
Database agent for SQLite database operations.
"""

import logging
import sqlite3
import os


class DB_Agent:  # Database agent
    def __init__(self, db_name):
        """
        Initialize the database agent with the path to the database file.

        Args:
            db_name (str): Path to the database file (or name)

        Returns:
            DB_Agent (DB_Agent): The database agent object
        """
        self.db_name = os.path.abspath(db_name)  # Path to the database file (or name)
        self.conn = None  # Connection to the database
        self.cursor = None  # Cursor for executing SQL commands

        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)  # Configure logging


    def __del__(self):  # Destructor, make sure to close the connection once the object is deleted
        """
        Destructor to close the database connection.
        """
        if self.conn:
            self.conn.close()


    def connect(self):
        """
        Connect to the SQLite database.
        """
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
        """
        Disconnect from the SQLite database.
        """
        if self.conn:  # Check if there is a connection to the database
            self.conn.close()  # Close the connection
            self.logger.info("Disconnected from the database successfully.")
            self.conn = None  # Reset the connection and cursor objects
            self.cursor = None  
        else:
            self.logger.warning("No connection to the database.")


    def initialize_db(self, schema_path):
        """
        Create the database schema.
        
        Args:
            schema_path (str): Path to the SQL file containing the schema
        """
        self.connect()  # Connect to the database
        try:
            # Read the schema from the provided file
            with open(schema_path, 'r') as f:
                schema = f.read()  # Read the SQL commands from the file

            self.cursor.executescript(schema)  # Execute the SQL commands
            self.conn.commit()  # Commit the changes
            self.logger.info("Database schema created successfully.")
        except Exception as e:  
            self.logger.error(f"Error initializing the database schema: {e}")
            if self.conn:
                self.conn.rollback()  # Rollback any changes if an error occurred
        finally:
            self.disconnect()  # Always disconnect after use


    def nuke_db(self):  # WARNING: Use this only as DEBUG during development
        """
        Completely remove the database and all of the data.
        """
        self.disconnect()  # Make sure the connection is severed
        try:
            os.remove(self.db_name)  # Delete the database file
            self.logger.info("Database nuked successfully.")
        except Exception as e:
            self.logger.error(f"Error nuking the database: {e}")

    
    def execute(self, sql, params=None):  # Generic method to execute SQL commands
        """
        Execute an SQL command with optional parameters.
        
        Args:
            sql (str): SQL command to execute
            params (tuple): Parameters to pass to the SQL command
        """
        self.connect()  # Connect to the database
        try:
            if params:  # If parameters are provided
                self.cursor.execute(sql, params)  # Execute the command with parameters
            else:
                self.cursor.execute(sql)  # Execute the command without parameters
            self.conn.commit()  # Commit the changes
            self.logger.info("SQL command executed successfully.")
        except Exception as e:
            self.logger.error(f"Error executing SQL '{sql}' with params {params}: {e}")
            if self.conn:
                self.conn.rollback()
        finally:
            self.disconnect()

    
    def fetch(self, sql, params=None):  # Generic method to fetch data from the database
        """
        Fetch data from the database using an SQL query with optional parameters.
        
        Args:
            sql (str): SQL query to execute
            params (tuple): Parameters to pass to the SQL query

        Returns:
            data (list): List of tuples containing the fetched data
        """
        self.connect()
        data = None
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            data = self.cursor.fetchall()  # Fetch all the data
            self.logger.info("Data fetched successfully.")
        except Exception as e:
            self.logger.error(f"Error fetching data with SQL '{sql}' and params {params}: {e}")
        finally:
            self.disconnect()
            return data

    
    def insert(self, table, data): # Insert helper
        """
        Insert data into a table.
        
        Args:
            table (str): Name of the table to insert data into
            data (dict): Dictionary containing the data to insert
        """
        self.connect()
        try:
            columns = ', '.join(data.keys())  # Get the column names by joining the keys
            placeholders = ', '.join(['?' for _ in data.values()])  # Create placeholders for the values
            sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"  # Create the SQL command to insert data
            self.cursor.execute(sql, tuple(data.values()))  # Execute the command with the values
            self.conn.commit()  # Commit the changes
            self.logger.info(f"Inserted record into {table}: {data}")
        except Exception as e:
            self.logger.error(f"Error inserting data into {table}: {e}")
            if self.conn:
                self.conn.rollback()
        finally:
            self.disconnect()
    

    def update(self, table, data, condition):  # Update helper
        """
        Update data in a table based on a condition.
        
        Args:
            table (str): Name of the table to update
            data (dict): Dictionary containing the data to update
            condition (str): Condition to filter the rows to update
        """
        self.connect()
        try:
            set_clause = ', '.join([f"{key} = ?" for key in data.keys()])  # Create the SET clause
            sql = f"UPDATE {table} SET {set_clause} WHERE {condition}"  # Create the SQL command to update data
            self.cursor.execute(sql, tuple(data.values()))  # Execute the command with the values
            self.conn.commit()  # Commit the changes
            self.logger.info(f"Updated record in {table}: {data}")
        except Exception as e:
            self.logger.error(f"Error updating data in {table}: {e}")
            if self.conn:
                self.conn.rollback()
        finally:
            self.disconnect()

    
    def delete(self, table, condition):  # Delete helper
        """
        Delete data from a table based on a condition.
        
        Args:
            table (str): Name of the table to delete data from
            condition (str): Condition to filter the rows to delete
        """
        self.connect()
        try:
            sql = f"DELETE FROM {table} WHERE {condition}"  # Create the SQL command to delete data
            self.cursor.execute(sql)  # Execute the command
            self.conn.commit()  # Commit the changes
            self.logger.info(f"Deleted record from {table}.")
        except Exception as e:
            self.logger.error(f"Error deleting data from {table}: {e}")
            if self.conn:
                self.conn.rollback()
        finally:
            self.disconnect()

    
    def bulk_insert(self, table, columns, values):  # Bulk insert helper
        """
        Bulk insert data into a table.

        Args:
            table (str): Name of the table to insert data into
            columns (list): List of column names
            values (list): List of tuples containing the values to insert
        """
        self.connect()
        try:
            placeholders = ', '.join(['?' for _ in columns])  # Create placeholders for the values
            sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"  # Create the SQL command
            self.cursor.executemany(sql, values)  # Execute the command with multiple values
            self.conn.commit()  # Commit the changes
            self.logger.info(f"Bulk inserted {len(values)} records into {table}.")
        except Exception as e:
            self.logger.error(f"Error bulk inserting data into {table}: {e}")
            if self.conn:
                self.conn.rollback()
        finally:
            self.disconnect()

    
    def table_exists(self, table_name):
        """
        Check if a table exists in the database.
        
        Args:
            table_name (str): Name of the table to check
        
        Returns:
            exists (bool): True if the table exists, False otherwise
        """
        self.connect()
        exists = False
        try:
            sql = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"  # SQL command to check if the table exists
            self.cursor.execute(sql)  # Execute the command
            if self.cursor.fetchone():  # Fetch the result and check if the table exists
                exists = True
            self.logger.info(f"Table {table_name} exists: {exists}")
        except Exception as e:
            self.logger.error(f"Error checking if table {table_name} exists: {e}")
        finally:
            self.disconnect()
            return exists
