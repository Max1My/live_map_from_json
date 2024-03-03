# live_map_from_json

## About

This is a simple mini project for displaying coordinates on a map using Flask, Kafka, Leaflet


## Requirements

Firstly for example you use [Kafka Stack Docker Compose](https://github.com/conduktor/kafka-stack-docker-compose)

Secondly install requirements

 ```
pip install -r requirements.txt
 ```

Create json from in `example_data`


For example, you can create them on [geojson.io](https://geojson.io/)


## Usage

For create message use:

```
python producer.py <topic_name> <number_line>
```

Run Flask:

```
python app.py
```