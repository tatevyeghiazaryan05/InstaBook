from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.endpoints import user_auth, user_crud, posts_crud


app = FastAPI()

app.mount("/user_pics", StaticFiles(directory="user_pics"), name="user_pics")
# app.mount("/post_images", StaticFiles(directory="/app/api/endpoints/post_images"), name="post_images")


app.include_router(user_auth.user_auth_router)
app.include_router(user_crud.user_crud_router)
app.include_router(posts_crud.post_crud_router)
