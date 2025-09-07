from dotenv import load_dotenv
import os
import psycopg2

def connect_to_db():
    """Establish a connection to the PostgreSQL database."""
    load_dotenv()
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            database=os.getenv("POSTGRES_NAME"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )
        print("Connection to database established.")
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None