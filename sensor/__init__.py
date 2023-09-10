# create FastAPI instance
from fastapi_mqtt import FastMQTT, MQTTConfig
import motor.motor_asyncio
from redis import StrictRedis
from fastapi import FastAPI

app = FastAPI()

# mqtt connection
mqtt_config = MQTTConfig(host="mqtt5", port=1883)
mqtt = FastMQTT(config=mqtt_config)
mqtt.init_app(app)

# mongo db connection
mongo_client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://root:example@mongo:27017")
database = mongo_client.exalon

# redis connection
redis = StrictRedis(host="redis", port=6379)
