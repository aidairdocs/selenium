# E:\CRM\automation_project\paddleocr_db_manager.py

import psycopg2

DATABASE_USER = "denis"
DATABASE_HOST = "localhost"
DATABASE_NAME = "ai_training"
DATABASE_PASSWORD = "De319402939!"
DATABASE_PORT = 5432

def get_paddleocr_connection():
    """
    Returns a psycopg2 connection to the 'ai_training' DB
    where we have our 'paddleocr_training_data' table.
    """
    return psycopg2.connect(
        user=DATABASE_USER,
        host=DATABASE_HOST,
        database=DATABASE_NAME,
        password=DATABASE_PASSWORD,
        port=DATABASE_PORT
    )
