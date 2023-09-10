# Sensor Data Monitoring System

This project simulates the behavior of sensors, monitors their readings, and provides APIs to retrieve data based on specific criteria. It utilizes Docker for easy deployment and management of services.

## Components

### MQTT Broker (Mosquitto)
- A Mosquitto MQTT broker is deployed using Docker to facilitate communication between sensors and the data storage component.

### MQTT Publisher (Python MQTT Client)
- A Python MQTT client publishes simulated sensor readings to topics like `sensors/temperature` and `sensors/humidity`. The data is formatted as JSON payloads.

### MQTT Subscriber (Python MQTT Client)
- Another Python MQTT client acts as a subscriber, receiving messages published by sensors. It stores the received messages in a MongoDB collection and push the latesh 10 reading in redis.

### Data Storage (MongoDB)
- A MongoDB instance is initiated using Docker to save the incoming MQTT messages. These messages include sensor ID, reading value, and timestamp.

### In-Memory Data Management (Redis)
- Redis, also Dockerized, is used to store the latest ten sensor readings in memory for quick retrieval.

### FastAPI Endpoint
- A FastAPI-based RESTful API provides the following endpoints:
  - `GET /`: Root api endpoint here I am creating some mimic reading and publish it to subsciber
  - `GET /sensor-readings`: Fetch sensor readings by specifying a start and end range.
  - `GET /latest-readings/{sensor_id}`: Retrieve the last ten sensor readings for a specific sensor.

### Docker Integration (Docker Compose)
- Docker Compose is used to manage and orchestrate all services, making it easy to start and stop the entire system.

## Usage

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/sensor-monitoring.git
   ```

2. Navigate to the project directory:

   ```
   cd exelon-assingment
   ```

3. Start the services using Docker Compose:

   ```
   docker-compose up --build
   ```

4. Access the FastAPI API at `http://localhost:8000`.

## API Endpoints

### 1. Root Endpoint

The root endpoint of the API provides basic information about the available sensors and the status of the service.

- **Endpoint**: `GET /`
- **Response**:
  ```json
  {
      "status": true,
      "sensor_id": [
          "sensor1",
          "sensor2",
          "sensor3"
      ]
  }
  ```

This root endpoint will generate a random reading of temperature and humidity and publish those reading on this two topics such as `sensors/humidity/#` and `temperature/humidity/#` and will return the available sensor Id's in response.

### 2. Fetch Sensor Readings

- **Endpoint**: `POST /sensor-readings`
- **Request Payload**:
  ```json
  {
      "type": "temperature",
      "sensor_id": "sensor1",
      "sensor_start_range": 10,
      "sensor_end_range": 80
  }
  ```

- **Response**:
  ```json
  [
      {
          "sensor_id": "sensor1",
          "value": 42.45476492115209,
          "timestamp": "2023-09-10T08:19:18",
          "type": "temperature"
      },
      {
          "sensor_id": "sensor1",
          "value": 72.98519987740772,
          "timestamp": "2023-09-10T08:19:18",
          "type": "temperature"
      },
      {
          "sensor_id": "sensor1",
          "value": 58.45354986144849,
          "timestamp": "2023-09-10T08:19:18",
          "type": "temperature"
      },
      {
          "sensor_id": "sensor1",
          "value": 78.64631865069701,
          "timestamp": "2023-09-10T08:19:18",
          "type": "temperature"
      },
      // ... (other sensor readings within the specified range)
  ]
  ```

This endpoint allows you to retrieve sensor readings of a specific type (`temperature` in this example) within the range of values specified (from 10 to 80). The response includes the sensor ID, reading value, timestamp, and sensor type for each reading that falls within the specified range.

You can use this endpoint to filter sensor readings based on your specific criteria.
### 3. Retrieve Last Ten Sensor Readings for a Specific Sensor

- **Example**: `GET /latest-readings/`
- **Query Parameters**:
  - `sensor_id`: The unique ID of the sensor (e.g., `sensor1`).
  - `sensor_type`: The type of sensor readings (e.g., `temperature`).


- **Response**:
  ```json
  [
      {
          "sensor_id": "sensor1",
          "value": 0.020127990437934784,
          "timestamp": "2023-09-10T14:16:20",
          "type": "temperature"
      },
      {
          "sensor_id": "sensor1",
          "value": 10.638323006917794,
          "timestamp": "2023-09-10T14:16:20",
          "type": "temperature"
      },
      {
          "sensor_id": "sensor1",
          "value": 63.863479427789294,
          "timestamp": "2023-09-10T14:16:20",
          "type": "temperature"
      },
      {
          "sensor_id": "sensor1",
          "value": 28.419814019773394,
          "timestamp": "2023-09-10T14:16:20",
          "type": "temperature"
      },
      {
          "sensor_id": "sensor1",
          "value": 77.03386649226782,
          "timestamp": "2023-09-10T14:16:20",
          "type": "temperature"
      },
      {
          "sensor_id": "sensor1",
          "value": 39.573500178554376,
          "timestamp": "2023-09-10T14:16:20",
          "type": "temperature"
      },
      {
          "sensor_id": "sensor1",
          "value": 48.95130851961479,
          "timestamp": "2023-09-10T14:16:20",
          "type": "temperature"
      },
      {
          "sensor_id": "sensor1",
          "value": 42.43474294584313,
          "timestamp": "2023-09-10T14:16:20",
          "type": "temperature"
      },
      {
          "sensor_id": "sensor1",
          "value": 89.86048392828353,
          "timestamp": "2023-09-10T14:16:20",
          "type": "temperature"
      },
      {
          "sensor_id": "sensor1",
          "value": 26.123177053614278,
          "timestamp": "2023-09-10T14:14:19",
          "type": "temperature"
      }
  ]
  ```

This endpoint allows you to retrieve the latest ten sensor readings for a specific sensor and sensor type (e.g., `temperature`, `humidity`). The response includes the sensor ID, reading value, timestamp, and sensor type for each of the latest readings. You can use this endpoint to monitor the most recent sensor data for analysis or visualization purposes.

### File Structure

- `/sensor`: This directory contains the core components of the sensor service.
  - `/sensor/router.py`: Defines the FastAPI router for handling sensor data API endpoints.
  - `/sensor/serializer.py`: Contains the payload serializer for parsing incoming MQTT data.
  - `/sensor/__init__.py`: Initializes and configures the FastAPI instance, MQTT client for publishing and subscribing, MongoDB connection, and Redis instance for managing the latest sensor readings.

- `/app.py`: Configures the MQTT publisher and subscriber, includes the FastAPI router, and sets up the application.
- `Dockerfile`: Configure the docker image for the web-api
- `docker-compose.yml`: The `docker-compose.yml` file is used to define and manage multiple interconnected Docker containers as a service. In your case, you are configuring several services, including `web-api`, `mongodb`, `redis`, and `mqtt`

## Dependencies

- Docker and Docker Compose

- Python 3.x with fastapi_mqtt, motor(for mongodb), redis-py, and FastAPI libraries installed.

## Contributors

- Email: <siddheshangane142000@gmail.com>

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Note

Please use the Postman collection provided in this repository for testing the API endpoints. You can find the collection file at:

`/exalens api's.postman_collection.json`

Make sure to import the collection into your Postman workspace and configure the necessary environment variables for testing.
