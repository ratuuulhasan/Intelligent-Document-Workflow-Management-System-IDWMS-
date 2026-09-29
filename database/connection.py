import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="idwms",
        user="postgres",
        password="admin",
        cursor_factory=RealDictCursor
    )