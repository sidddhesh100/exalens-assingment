import motor.motor_asyncio
import os

MONGO_DETAILS = os.environ.get("DATABASE_URL")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.students

student_collection = database.get_collection("students_collection")