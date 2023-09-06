from pydantic import BaseModel


class Payload(BaseModel):
    type: str
    sensor_id: str
    sensor_start_range: int
    sensor_end_range: int
