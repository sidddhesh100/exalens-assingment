import json
import random
import time

import uvicorn
from fastapi import Response
from sensor import app, mqtt, redis, database
from sensor.router import sensor_route

# include routers
app.include_router(sensor_route)


@app.get("/")
def mimic_readings():
    sensor_ids = ["sensor1", "sensor2", "sensor3"]
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

    return Response(content=json.dumps({"status": True, "sensor_id": sensor_ids}), media_type="application/json")


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
    save_reading_in_db_redis(payload=payload, type="temperature")


@mqtt.subscribe("sensors/humidity/#")
async def humidity_to_topic(client, topic, payload, qos, properties):
    print("Received message to specific topic: ", topic, payload.decode(), qos, properties)
    save_reading_in_db_redis(payload=payload, type="humidity")


def save_reading_in_db_redis(payload, type):
    payload = json.loads(payload.decode())
    sensor_id = payload["sensor_id"]
    redis_key = f"{type}-{sensor_id}"
    redis.lpush(redis_key, json.dumps(payload))
    redis.ltrim(redis_key, 0, 9)
    database["sensor_reading"].insert_one(payload)


@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")


@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)


# if __name__ == "__main__":
#     uvicorn.run("server.app:app", host="0.0.0.0", port=8000, reload=True)
