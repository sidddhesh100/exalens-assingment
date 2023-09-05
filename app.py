import json
import random
import time
from typing import Union
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI, Response

# from paho.mqtt.client import mqtt
# from .settings import Settings
from fastapi_mqtt import FastMQTT, MQTTConfig

import motor.motor_asyncio
from redis import StrictRedis
import os

app = FastAPI()
# setting = Settings()

# mqtt_client = mqtt.Client()
# mqtt_client.connect(os.getenv('BROKER_ADDRESS'), os.getenv('BROKER_PORT'))

mqtt_config = MQTTConfig(username="root", password="example")

mqtt = FastMQTT(config=mqtt_config)

mqtt.init_app(app)

# import pdb; pdb.set_trace()
mongo_client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://root:example@localhost:27017")
database = mongo_client.exalon

redis = StrictRedis(host="localhost", port=6379)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/mimic_readings")
def mimic_readings():
    sensor_ids = ["sensor1", "sensor2", "sensor3"]
    try:
        i = 0
        while True:
            for sensor_id in sensor_ids:
                temperature_topic = f"sensors/temperature/{sensor_id}"
                humidity_topic = f"sensors/humidity/{sensor_id}"

                publish_sensor_reading(sensor_id, temperature_topic, "temperature")
                publish_sensor_reading(sensor_id, humidity_topic, "humidity")

                # time.sleep(5)  # Wait for 5 seconds before publishing again
                i += 1
                print(i)
                if i == 25:
                    break
            if i == 25:
                break
    except KeyboardInterrupt:
        print("Client stopped")
    return Response(content=json.dumps({"status": True}), media_type="application/json")


def publish_sensor_reading(sensor_id: str, topic: str, type: str) -> None:
    # Generate a random reading value
    reading_value = random.uniform(0, 100)

    # Create JSON payload
    payload = {"sensor_id": sensor_id, "value": reading_value, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"), "type": type}

    # Publish the payload to the topic
    mqtt.publish(topic, json.dumps(payload))
    print(f"Published: {payload}")


@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("/mqtt")  # subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)


@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ", topic, payload.decode(), qos, properties)
    return 0


@mqtt.subscribe("sensors/temperature/#")
async def temperature_to_topic(client, topic, payload, qos, properties):
    print("Received message to specific topic: ", topic, payload.decode(), qos, properties)
    payload = json.loads(payload.decode())
    sensor_id = payload["sensor_id"]
    redis_key = f"temperature-{sensor_id}"
    redis.lpush(redis_key, json.dumps(payload))
    redis.ltrim(redis_key, 0, 9)
    database["sensor_reading"].insert_one(payload)


@mqtt.subscribe("sensors/humidity/#")
async def humidity_to_topic(client, topic, payload, qos, properties):
    print("Received message to specific topic: ", topic, payload.decode(), qos, properties)
    payload = json.loads(payload.decode())
    sensor_id = payload["sensor_id"]
    redis_key = f"humidity-{sensor_id}"
    redis.lpush(redis_key, json.dumps(payload))
    redis.ltrim(redis_key, 0, 9)
    database["sensor_reading"].insert_one(payload)


@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")


@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)


class Payload(BaseModel):
    type: str
    sensor_id: str
    sensor_start_range: int
    sensor_end_range: int


@app.get("/get_last_10_records")
async def fetch_last_10_records(sensor_id: str, sensor_type: str) -> Response:
    """
    Fetch last 10 sensor readings from redis and return it in responose
    """
    redis_key = f"{sensor_type}-{sensor_id}"
    readings = redis.lrange(redis_key, 0, 9)
    data = [json.loads(value) for value in readings]
    return Response(content=json.dumps(data), media_type="application/json")


@app.post("/get_readings")
async def get_specific_readings(payload: Payload):
    """
    fetch reading in specific range for the humidity or temperature on the basis of user input
    """
    query = database["sensor_reading"].find(
        {
            "sensor_id": payload.sensor_id,
            "type": payload.type,
            "value": {"$lte": payload.sensor_end_range, "$gte": payload.sensor_start_range},
        },
        {"_id": 0},
    )
    data = []
    async for document in query:
        data.append(document)
    return Response(content=json.dumps(data), media_type="application/json")


if __name__ == "__main__":
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000, reload=True)
