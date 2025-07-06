import os
import shutil
from datetime import datetime
from fastapi import UploadFile, HTTPException, status

from db_connection import DbConnection
from schemas.posts_schema import ChangeDescription, ChangeLocation


class PostCrud:
    def __init__(self):
        self.db = DbConnection()

    def create_post(self, user_id: int, image: UploadFile, description: str, location: str, is_public: bool):
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Only image files are allowed")

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        upload_dir = os.path.join(BASE_DIR, "..", "post_images")
        os.makedirs(upload_dir, exist_ok=True)

        ext = image.filename.split(".")[-1]
        filename = f"post_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
        file_path = os.path.join(upload_dir, filename)

        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Failed to save image")

        image_url = f"http://localhost:8000/post_images/{filename}"

        try:
            self.db.cursor.execute(
                                    """INSERT INTO posts (user_id, image,
                                    description, location, is_public)
                                    VALUES (%s, %s, %s, %s, %s)""",
                                    (user_id, image_url, description, location, is_public))
            self.db.conn.commit()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Database insert error")

    def change_post_description(self, data: ChangeDescription):
        new_description = data.description
        post_id = data.post_id
        try:
            self.db.cursor.execute("""UPDATE posts SET description=%s WHERE id=%s""",
                               (new_description, post_id))
            self.db.conn.commit()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error updating")

    def change_post_location(self, data: ChangeLocation):
        new_location = data.location
        post_id = data.post_id
        try:
            self.db.cursor.execute("""UPDATE posts SET location=%s WHERE id=%s""",
                                   (new_location, post_id))
            self.db.conn.commit()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error updating")

    def delete_post(self, post_id: int):
        try:
            self.db.cursor.execute("DELETE FROM posts WHERE id=%s",
                                   (post_id,))
            self.db.conn.commit()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error deleting")

    def get_post(self, post_id: int):
        try:
            self.db.cursor.execute("SELECT * FROM posts WHERE id=%s",
                                   (post_id,))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error in select")
        try:
            post = self.db.cursor.fetchone()
            return post
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="fetch error")

