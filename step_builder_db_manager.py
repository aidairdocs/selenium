# E:\CRM\automation_project\step_builder_db_manager.py

import os
import psycopg2
from dotenv import load_dotenv

# If your .env is in a specific location, provide the exact path:
# load_dotenv(r"E:\CRM\automation_project\.env")

# Otherwise, if .env is in the current working directory or parent folder,
# you can just do:
load_dotenv()

DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_PORT = os.getenv("DATABASE_PORT")

def get_connection():
    return psycopg2.connect(
        user=DATABASE_USER,
        host=DATABASE_HOST,
        database=DATABASE_NAME,
        password=DATABASE_PASSWORD,
        port=DATABASE_PORT
    )
