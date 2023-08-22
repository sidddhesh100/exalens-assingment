from typing import Union
import uvicorn
from fastapi import FastAPI
from .settings import Settings

app = FastAPI()
setting = Settings()

database_url = os.environ.get("DATABASE_URL")
debug_mode = os.environ.get("DEBUG")
secret_key = os.environ.get("SECRET_KEY")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000, reload=True)
