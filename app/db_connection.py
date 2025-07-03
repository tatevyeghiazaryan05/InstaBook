import psycopg2
from psycopg2.extras import RealDictCursor


class DbConnection:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            port=5432,
            user="postgres",
            database="instabook",
            password="password",
            cursor_factory=RealDictCursor
        )

        self.cursor = self.conn.cursor()
