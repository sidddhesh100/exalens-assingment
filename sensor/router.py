from fastapi import APIRouter, Response
from . import redis, database
import json
from .serializer import Payload


sensor_route = APIRouter(prefix="/sensor")


@sensor_route.get("/latest-readings")
async def fetch_last_10_records(sensor_id: str, sensor_type: str) -> Response:
    """
    Fetch last 10 sensor readings from redis and return it in responose
    """
    redis_key = f"{sensor_type}-{sensor_id}"
    readings = redis.lrange(redis_key, 0, 9)
    data = [json.loads(value) for value in readings]
    return Response(content=json.dumps(data), media_type="application/json")


@sensor_route.post("/get_readings")
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
