import os
import shutil
from datetime import datetime
from fastapi import UploadFile, HTTPException, status

from db_connection import DbConnection
from schemas.posts_schema import CreatePostSchema, UpdatePostSchema


class PostCrud:
    def __init__(self):
        self.db = DbConnection()

    def create_post(self, data: CreatePostSchema, user_id: int):
        try:
            self.db.cursor.execute(
                                    """INSERT INTO posts (user_id, image_url,
                                    description, location, is_public)
                                    VALUES (%s, %s, %s, %s, %s)""",
                                    (user_id, data.image_url, data.description,
                                     data.location, data.is_public))
            self.db.conn.commit()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Database insert error")

    def update_post(self, data: UpdatePostSchema, user_id: int):
        try:
            self.db.cursor.execute("SELECT user_id FROM posts WHERE id = %s", (data.post_id,))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Query error")

        try:
            post = self.db.cursor.fetchone()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Fetch error")

        if not post or post["user_id"] != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this post")

        description = data.description if data.description else post["description"]
        location = data.location if data.location else post["location"]
        try:
            self.db.cursor.execute("""UPDATE posts SET 
            description = %s, location = %s WHERE id = %s""",
                                   (description, location, data.post_id))

            self.db.conn.commit()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Failed to update post")

    def get_post(self, post_id: int):
        try:
            self.db.cursor.execute("SELECT * FROM posts WHERE id=%s",
                                   (post_id,))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error in select")
        try:
            post = self.db.cursor.fetchone()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="fetch error")
        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return post

    def delete_post(self, post_id: int, user_id: int):
        post = self.get_post(post_id)
        print(post)
        image_url = dict(post).get("image")
        print(image_url)
        image_name = image_url.split("/")[-1]

        file_path = os.path.join("post_images", image_name)
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            print(file_path)

        try:
            self.db.cursor.execute("DELETE FROM posts WHERE id=%s AND user_id=%s",
                                   (post_id, user_id))
            self.db.conn.commit()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error deleting")
