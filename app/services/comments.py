from fastapi import HTTPException, status

from db_connection import DbConnection
from schemas.posts_schema import CommentSchema, UpdateCommentSchema


class Comment:
    def __init__(self):
        self.db = DbConnection()

    def write_comment(self, data: CommentSchema, user_id: int):
        post_id = data.post_id
        comment = data.comment
        try:
            self.db.cursor.execute("""INSERT INTO comments (post_id,user_id,comment) VALUES (%s,%s,%s)""",
                                   (post_id, user_id, comment))
            self.db.conn.commit()
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database Query error"
            )

    def get_comments_for_post(self, post_id: int):
        try:
            self.db.cursor.execute("""SELECT * FROM comments WHERE post_id = %s""",
                                   (post_id,))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Query error")

        try:
            comments = self.db.cursor.fetchall()
            return comments
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Fetch error")

    def delete_comment(self, comment_id: int, user_id: int):
        try:
            self.db.cursor.execute("""SELECT user_id, post_id FROM comments WHERE id = %s""", (comment_id,))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Query error")

        try:
            comment = self.db.cursor.fetchone()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Fetch error")

        if not comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Comment not found")

        comment_user_id = comment["user_id"]
        post_id = comment["post_id"]

        try:
            self.db.cursor.execute("""SELECT user_id FROM posts WHERE id = %s""", (post_id,))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Query error")

        try:
            post = self.db.cursor.fetchone()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Fetch error")

        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Post not found")

        post_owner_id = post["user_id"]

        if user_id != comment_user_id and user_id != post_owner_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to delete this comment")

        try:
            self.db.cursor.execute("""DELETE FROM comments WHERE id = %s""", (comment_id,))
            self.db.conn.commit()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Query error")

    def update_comment(self, comment_id: int, user_id: int, data: UpdateCommentSchema):
        try:
            self.db.cursor.execute("""SELECT user_id FROM comments WHERE id = %s""", (comment_id,))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Query error")

        try:
            owner = self.db.cursor.fetchone()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Fetch error")
        if not owner:
            raise HTTPException(status_code=404, detail="Comment not found")
        if owner["user_id"] != user_id:
            raise HTTPException(status_code=403, detail="Not authorized")

        try:
            self.db.cursor.execute("""UPDATE comments SET 
                                    comment = %s WHERE id = %s""",
                                   (data.comment, comment_id))
            self.db.conn.commit()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Failed to update comment")

    def like_comment(self, comment_id, user_id: int):
        try:
            self.db.cursor.execute("SELECT id FROM comments WHERE id = %s", (comment_id,))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Query error")

        try:
            comment = self.db.cursor.fetchone()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error fetching")

        if not comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Comment not found")

        try:
            self.db.cursor.execute("""INSERT INTO comment_likes (comment_id, user_id)
                                   VALUES (%s, %s)""", (comment_id, user_id))
            self.db.conn.commit()
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="You already liked this comment")

    def unlike_comment(self, comment_id, user_id: int):
        try:
            self.db.cursor.execute("""DELETE FROM comment_likes WHERE 
                                   comment_id = %s AND user_id = %s""",
                                   (comment_id, user_id))

            self.db.conn.commit()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Failed to unlike comment")

    def get_comment_likes(self, comment_id: int):
        try:
            self.db.cursor.execute(
                "SELECT COUNT(*) FROM comment_likes WHERE comment_id = %s",
                (comment_id,)
            )
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Failed to select")

        try:
            count = self.db.cursor.fetchone()["count"]
            return {"total_likes": count}
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Failed to fetch")
