import json
import random
import time
from typing import Union
import uvicorn
from fastapi import FastAPI, Response

# from paho.mqtt.client import mqtt
# from .settings import Settings
from fastapi_mqtt import FastMQTT, MQTTConfig

import motor.motor_asyncio
from redis import Redis
import os

app = FastAPI()
# setting = Settings()

# mqtt_client = mqtt.Client()
# mqtt_client.connect(os.getenv('BROKER_ADDRESS'), os.getenv('BROKER_PORT'))

mqtt_config = MQTTConfig(username=os.getenv("USERNAME"), password=os.getenv("PASSWORD"))

mqtt = FastMQTT(config=mqtt_config)

mqtt.init_app(app)


mongo_client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_DB_URL"))
database = mongo_client.exalon

redis = Redis(host="localhost", port=os.getenv("REDIS_PORT"), db=0)


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

                publish_sensor_reading(sensor_id, temperature_topic)
                publish_sensor_reading(sensor_id, humidity_topic)

                time.sleep(5)  # Wait for 5 seconds before publishing again
            print()
            print(i)
    except KeyboardInterrupt:
        print("Client stopped")
    return Response(content={"status": True}, media_type="application/json")


def publish_sensor_reading(sensor_id, topic):
    # Generate a random reading value
    reading_value = random.uniform(0, 100)

    # Create JSON payload
    payload = {
        "sensor_id": sensor_id,
        "value": reading_value,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }

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


@mqtt.subscribe("my/mqtt/topic/#")
async def message_to_topic(client, topic, payload, qos, properties):
    print(
        "Received message to specific topic: ", topic, payload.decode(), qos, properties
    )
    database["sensor_reading"].insert_one(payload)


@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")


@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)


if __name__ == "__main__":
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000, reload=True)
