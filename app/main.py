from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.endpoints import user_auth, user_crud


app = FastAPI()

app.mount("/user_pics", StaticFiles(directory="user_pics"), name="user_pics")


app.include_router(user_auth.user_auth_router)
app.include_router(user_crud.user_crud_router)
