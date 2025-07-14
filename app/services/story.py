# services/story_service.py

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

