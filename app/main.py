from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import asyncio
from services.comments import Comment

from api.endpoints import (user_auth, user_crud, posts_crud, save_posts,
                           comments, like, follow, story)


app = FastAPI()

# app.mount("/user_pics", StaticFiles(directory="user_pics"), name="user_pics")
# app.mount("/post_images", StaticFiles(directory="/app/api/endpoints/post_images"), name="post_images")


@app.on_event("startup")
async def start_background_tasks():
    comment_service = Comment()
    asyncio.create_task(comment_service.auto_clean_orphaned_comment_likes())

app.include_router(user_auth.user_auth_router)
app.include_router(user_crud.user_crud_router)
app.include_router(posts_crud.post_crud_router)
app.include_router(save_posts.save_post_router)
app.include_router(comments.comment_router)
app.include_router(like.like_router)
app.include_router(follow.follow_router)
app.include_router(story.story_router)
