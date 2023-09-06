# create FastAPI instance
from fastapi_mqtt import FastMQTT, MQTTConfig
import motor.motor_asyncio
from redis import StrictRedis
from fastapi import FastAPI

app = FastAPI()

# mqtt connection
mqtt_config = MQTTConfig(username="root", password="example")
mqtt = FastMQTT(config=mqtt_config)
mqtt.init_app(app)

# mongo db connection
mongo_client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://root:example@localhost:27017")
database = mongo_client.exalon

# redis connection
redis = StrictRedis(host="localhost", port=6379)

# include routers
