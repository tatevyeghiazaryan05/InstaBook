import os
import shutil
from datetime import datetime, timedelta

from fastapi import UploadFile, HTTPException, status

from db_connection import DbConnection
from schemas.story_schema import StorySchema


class StoryService:
    def __init__(self):
        self.db = DbConnection()
        self.media_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "story_media")

    def create_story(self, user_id: int, file: UploadFile, data: StorySchema):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        upload_dir = os.path.join(BASE_DIR, "story_media")
        os.makedirs(upload_dir, exist_ok=True)

        ext = file.filename.split('.')[-1]
        filename = f"story_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
        file_path = os.path.join(upload_dir, filename)

        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Failed to save story media")

        media_url = f"http://localhost:8000/api/get/image/{filename}"
        expires_at = datetime.now() + timedelta(minutes=1)

        try:
            self.db.cursor.execute("""INSERT INTO stories
                                  (user_id, media_url, caption,
                                  expires_at, is_video, is_public)
                                  VALUES (%s, %s, %s, %s, %s, %s)""",
                                   (user_id, media_url, data.caption,
                                    expires_at, data.is_video, data.is_public))
            self.db.conn.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"DB insert error: {e}")

        return {"message": "Story uploaded ✅"}

    def delete_expired_stories(self):
        try:
            self.db.cursor.execute("""SELECT NOW()::timestamp;""")
            time = self.db.cursor.fetchone()
            print(time)

        except Exception:
            pass
        try:
            self.db.cursor.execute("SELECT id, media_url FROM stories WHERE expires_at <= NOW()::timestamp")
            expired_stories = self.db.cursor.fetchall()
            print(expired_stories)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error fetching expired stories: {e}")

        deleted_count = 0
        for story in expired_stories:
            story_id = story["id"]
            media_filename = story["media_url"]
            file_path = os.path.join(self.media_folder, media_filename)

            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Warning: Could not delete file {file_path}: {e}")
            else:
                print(f"File not found or already deleted: {file_path}")

            try:
                self.db.cursor.execute("DELETE FROM stories WHERE id = %s", (story_id,))
                self.db.conn.commit()
                deleted_count += 1
            except Exception as e:
                print(f"Error deleting story ID {story_id} from DB: {e}")

        return {"message": f"{deleted_count} expired stories deleted successfully."}

    def get_story(self, story_id):
        try:
            self.db.cursor.execute("""SELECT * FROM stories WHERE id=%s""",(story_id,))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Query error")
        try:
            story = self.db.cursor.fetchone()
            return story
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Error fetching  stories")

    def view_story(self, story_id: int, user_id: int,):
        try:
            query = """
                INSERT INTO story_views (story_id, viewer_id)
                SELECT %s, %s
                WHERE NOT EXISTS (
                    SELECT 1 FROM story_views WHERE story_id = %s AND viewer_id = %s
                )
            """
            self.db.cursor.execute(query, (story_id, user_id, story_id, user_id))
            self.db.conn.commit()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Could not save story view")

    def get_story_viewers(self, story_id: int, user_id: int):
        try:
            self.db.cursor.execute("SELECT user_id FROM stories WHERE id = %s", (story_id,))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Query error")
        try:
            owner = self.db.cursor.fetchone()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Fetch error")

        if not owner or owner[0] != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="You are not the owner of this story")

        try:
            self.db.cursor.execute("""
                SELECT users.id, users.username, users.profile_image_url
                FROM story_views
                JOIN users ON story_views.viewer_id = users.id
                WHERE story_views.story_id = %s
            """, (story_id,))
            return self.db.cursor.fetchall()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error fetching viewers")

    def get_story_view_count(self, story_id: int, user_id: int):
        try:
            self.db.cursor.execute("SELECT user_id FROM stories WHERE id = %s", (story_id,))
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Query error")

        try:
            owner = self.db.cursor.fetchone()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Fetch error")

        if not owner or owner[0] != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="You are not the owner of this story")

        try:
            self.db.cursor.execute("SELECT COUNT(*) FROM story_views WHERE story_id = %s",
                                   (story_id,))
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database query error"
            )

        try:
            count = self.db.cursor.fetchone()
            return count
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch"
            )
