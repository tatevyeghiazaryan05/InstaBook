from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def get():
    return "a"
