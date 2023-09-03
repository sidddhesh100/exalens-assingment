from fastapi import APIRouter, Response

router = APIRouter(prefix="/sensor")


@router.get("/get_last_10_records")
async def fetch_last_10_records():
    """
    Fetch last 10 sensor readings from redis and return it in responose
    """
    data = {}

    return Response(content=data, media_type="application/json")


@router.post("/get_readings")
async def get_specific_readings():
    """
    fetch reading in specific range for the humidity or temperature on the basis of user input
    """
    data = {}
    return Response(content=data, media_type="application/json")
