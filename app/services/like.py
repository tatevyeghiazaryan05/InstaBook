from fastapi import HTTPException, status

from db_connection import DbConnection
from schemas.posts_schema import CommentSchema, UpdateCommentSchema


class Like:
    def __init__(self):
        self.db = DbConnection()

    def like_post(self, user_id: int, post_id: int):
        try:
            self.db.cursor.execute("""SELECT id FROM post_likes
                                   WHERE user_id = %s AND post_id = %s""",
                                   (user_id, post_id))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Query error")
        try:
            existing = self.db.cursor.fetchone()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Fetch error")

        if existing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="You already liked this post.")

        try:
            self.db.cursor.execute("""INSERT INTO post_likes (user_id, post_id) VALUES (%s, %s)""",
                                   (user_id, post_id))
            self.db.conn.commit()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Query error")

    def unlike_post(self, user_id: int, post_id: int):
        try:
            self.db.cursor.execute("""DELETE FROM post_likes WHERE 
                                   user_id = %s AND post_id = %s""",
                                   (user_id, post_id))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Query error")

        if self.db.cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Like not found")
        self.db.conn.commit()

    def count_likes(self, post_id: int):
        try:
            self.db.cursor.execute("""SELECT COUNT(*) FROM post_likes WHERE post_id = %s""",
                                   (post_id,))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Query error")

        try:
            count = self.db.cursor.fetchone()
            return count
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Fetch error")
