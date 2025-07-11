from fastapi import HTTPException, status

from db_connection import DbConnection


class Follow:
    def __init__(self):
        self.db = DbConnection()

    def follow(self, who:int, whom: int):
        try:
            self.db.cursor.execute("""SELECT * FROM follow WHERE who=%s AND whom=%s""",
                                   (who, whom))
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database Query error"
            )
        try:
            follow_data = self.db.cursor.fetchone()
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Fetch error"
            )
        if follow_data:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="You are also follow that user")

        try:
            self.db.cursor.execute("""INSERT INTO follow (who,whom) VALUES (%s,%s)""",
                                   (who, whom))
            self.db.conn.commit()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Query error")

    def unfollow(self, who: int, whom: int):
        try:
            self.db.cursor.execute("""DELETE FROM follow where who=%s AND whom=%s""",
                                   (who, whom))
            self.db.conn.commit()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Query error")
