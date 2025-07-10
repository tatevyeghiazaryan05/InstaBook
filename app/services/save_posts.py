from datetime import datetime, timedelta

from fastapi import HTTPException, status

from db_connection import DbConnection
from schemas.posts_schema import SavePostSchema
from core.security import pwd_context
from services.email_service import send_verification_email, generate_verification_code
from core.security import create_access_token


class SavePosts:
    def __init__(self):
        self.db = DbConnection()

    def save_post(self, data: SavePostSchema, user_id: int):
        post_id = data.post_id
        try:
            self.db.cursor.execute("""SELECT * FROM saveposts 
                                    WHERE user_id = %s AND post_id = %s""",
                                   (user_id, post_id))
            existing = self.db.cursor.fetchone()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You already saved this post."
                )
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Query error")

        try:
            self.db.cursor.execute("""INSERT INTO saveposts (post_id,user_id) VALUES (%s,%s)""",
                                   (post_id, user_id))
            self.db.conn.commit()
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database Query error :"
            )

    def get_saved_posts(self, user_id: int):
        try:
            self.db.cursor.execute("""SELECT * FROM saveposts WHERE user_id=%s""",
                                   (user_id,))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Query error")

        try:
            posts = self.db.cursor.fetchall()
            return posts
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Fetch error")

    def unsave_post(self, post_id: int, user_id: int):
        try:
            self.db.cursor.execute("""DELETE FROM saveposts 
                                    WHERE user_id = %s AND post_id = %s""",
                                   (user_id, post_id))
            self.db.conn.commit()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Unsave failed")
