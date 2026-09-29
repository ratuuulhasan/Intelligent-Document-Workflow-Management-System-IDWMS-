import psycopg2
from psycopg2.extras import RealDictCursor
from config import *

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        cursor_factory=RealDictCursor
    )

def test_connection():
    try:
        conn = get_connection()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False