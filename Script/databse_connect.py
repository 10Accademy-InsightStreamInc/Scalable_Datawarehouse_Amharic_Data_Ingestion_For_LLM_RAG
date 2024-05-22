import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv
from pathlib import Path

def main() -> None:
    """

    """
    env_path = Path('.env')
    load_dotenv(env_path)
    
    db_name: str = os.getenv('DB_DATABASE')
    port: str = os.getenv('DB_PORT')
    password: str = os.getenv('DB_PASSWORD')
    host: str = os.getenv('DB_HOST')
    user: str = os.getenv('DB_USERNAME')
    
    conn = psycopg2.connect(host=host, database=db_name, user=user, password=password, port=port)
    cursor = conn.cursor()
    
    with open('scripts/schema.sql', 'r') as schema_file:
        script: str = schema_file.read()
        cursor.execute(script)
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()