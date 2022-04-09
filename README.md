<div id="top"></div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-task">About The Task</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#structure">Structure</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#further-discussions">Further Discussions</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Task

### Instructions:

You will have to define the terms in which you understand the assignment. There are no definitive answers
to the case. If you have any doubts, make the reservations and assumptions which are necessary. We do
not expect you to deliver the definitive answer to all aspects of the case, but more to see your approach
and how you write your code (Maintainability, easy to read/understand and performance)

### Case

Objective

As a user of buses in Finland I want to be able to consume data for my mobile app that shows where each
bus is. I want to be able to search for buses close to me and show what their next stop is. If you come up
with other cases that I can use the data that could enhance my possibilities in the app, please add them as
well.

### Write a service that:
* Consumes telemetry from the MQTT server mqtt.hsl.fi
* Stores the telemetry
* Makes the telemetry searchable in a sane way through an API (http/gRPC/SignalR)
* Infrastructure needed to run the service (if any) should be hosted in docker

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With
* [ormar](https://collerek.github.io/ormar/)
* [FASTAPI](https://fastapi.tiangolo.com/)
* [paho-mqtt](https://pypi.org/project/paho-mqtt/)
* [PostgreSQL](https://www.postgresql.org/)

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Yun-no/IoTFinlandBuses.git
   ```
2. Build and run apps with Docker Compose
   ```sh
   docker-compose up -d --build
   ```

<!-- SERVICE STRUCTURE -->
## Structure
There are 3 Docker containers built to serve the application.
* a python-slim container act as mqtt client to consume telemetry
* a Postgres container to store the telemetry
* a python-slim container to create API on FASTAPI framework

### Structure diagram

[![Structure diagram][task-diagram]]


<!-- USAGE EXAMPLES -->
## Usage
Access RESTful API through
   ```sh
    curl -X 'POST' \
      'http://127.0.0.1:8008/api/v1/busaround' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "latitude_from": 60,
      "latitude_to": 65,
      "longitude_from": 24,
      "longitude_to": 26
    }'
   ```
Check the interactive documentations:

Swagger UI : http://127.0.0.1:8008/docs

ReDoc : http://127.0.0.1:8008/redoc


<p align="right">(<a href="#top">back to top</a>)</p>


<!-- Further discussion -->
## Further Discussions

### Database selection
The original plan was to use Redis for better performance. 
However instead of specific bus position lookup, flexible searching is needed.
A key-value db can't serve well for that use case.

PostgreSQL was then chosen for storing the data in a relational db.
And with the ORM package ormar combined with pydantic, data mapping and validation are automated.

### Data storing logic
The mqtt topic used is 
   ```sh
  /hfp/v2/journey/ongoing/vp/bus/#
   ```
It makes the client subscribed to all vehicle position messages from buses.

Whenever a new mqtt message arrive. A bus_id is generated from Unique ID of the operator combining Vehicle number -
referring the [documentation](https://digitransit.fi/en/developers/apis/4-realtime-api/vehicle-positions/) , "operator_id/vehicle_number uniquely identifies the vehicle."

The bus_id will be used for upsert action through INSERT ON CONFLICT statement in PostgreSQL.

It means the latest position message of every bus will be used to create record if not exist or update existing record in database. 

A quick research through Google tells that there was 19.1 thousand units(bus and coach) in Finland by 2019.
It's safe to assume that at most 30k records will be built in database over the time. 
We don't need to worry about oversize data storage with current solution (as historical data doesn't matter and get overwritten).

### Extra settings
Extra environment variables are specified in docker-compose file

NUMBER_OF_RECORDS=100

The number of records is used to limit the returned results. It can be further improved by pagination.

VALID_TIME_RANGE=5

The valid time range defines how long the API service would trace back to identify valid records, in minutes.
That means a bus position data that is not updated within last 5 minutes will be considered as not valid, thus not included in the API response.

### Further works and optimizations
* expand database to store more information from mqtt message
* improve the API service: add authentication/authorization, introduce rate limiting/pagination, allow more query parameters, build different endpoints
* implement gRPC for better internal communication performance
* add API gateway to offer end user more information combining the API response with data from other services: Routing API/Geocoding API
* forward MQTT messages to Apache Kafka for real time data processing/analysis
* store the MQTT messages to ElasticSearch as historical data for further usage

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
[task-diagram]: images/iot_task_diagram.png


