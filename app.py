from typing import Union
import uvicorn
from fastapi import FastAPI
from paho.mqtt.client import mqtt
from .settings import Settings
import motor.motor_asyncio
from redis import Redis


app = FastAPI()
setting = Settings()

mqtt_client = mqtt.Client()
mqtt_client.connect(setting.BROKER_ADDRESS, setting.BROKER_PORT)

mongo_client = motor.motor_asyncio.AsyncIOMotorClient(Settings.MONGO_DB_URL)
database = mongo_client.exalon

redis = Redis(host='localhost', port=setting.REDIS_PORT, db=0)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000, reload=True)
