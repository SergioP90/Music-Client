import logging
from db.db_agent import DB_Agent


# Set up logging configuration
logging.basicConfig(level=logging.DEBUG,  # Set the minimum level to capture
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler(),  # Output logs to console
                        logging.FileHandler('app.log')  # Save logs to a file
                    ])


def main():
    # Initialize the db agent and the database
    db_agent = DB_Agent('src/db/music.db')
    db_agent.initialize_db('src/db/database_schema.sql')

    #TODO: Remove the nuking of the database before deployment
    input("Enter to NUKE database...")
    # Nuke the database
    db_agent.nuke_db()  


if __name__ == "__main__":
    main()
