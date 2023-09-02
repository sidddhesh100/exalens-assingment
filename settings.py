from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # mqtt configuration
    BROKER_ADDRESS = "your_broker_ip"
    BROKER_PORT = 1883
    TEMPERATURE_TOPIC = 'sensors/temperature/'
    SENSOR_TOPIC = 'sensors/humidity/'
    
    # redis configuration
    REDIS_PORT = 6379
    
    # mongo db configuration
    MONGO_DB_URL = 'mongodb://root:example@localhost:27017/?authMechanism=DEFAULT'