import json
import sys
import time
import uuid
from datetime import datetime

from confluent_kafka import Producer

from confluent_kafka.admin import AdminClient

from admin_client import example_create_topics
from settings.config import get_config


def get_coordinates():
    input_file = open('./example_data/coordinates.json')
    json_array = json.load(input_file)
    coordinates = json_array['features'][0]['geometry']['coordinates']
    return coordinates


def delivery_callback(err, msg):
    if err:
        print('%% Message failed delivery: %s\n' % err)
    else:
        print('%% Message delivered to %s [%d] @ %d\n' %
              (msg.topic(), msg.partition(), msg.offset()))


def generate_checkpoint(coordinates: dict):
    i = 0
    while i < len(coordinates):
        data['key'] = data['busline'] + '_' + str(uuid.uuid4())
        data['timestamp'] = str(datetime.utcnow())
        data['latitude'] = coordinates[i][1]
        data['longitude'] = coordinates[i][0]
        message = json.dumps(data)
        try:
            p.produce(topic, message.encode('ascii'), callback=delivery_callback)
            time.sleep(1)

        except BufferError:
            print('%% Local producer queue is full (%d messages awaiting delivery): try again\n' %
                  len(p))
        p.poll(0)

        print('%% Waiting for %d deliveries\n' % len(p))
        p.flush()
        if i == len(coordinates) - 1:
            i = 0
        else:
            i += 1


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.stderr.write('Usage: %s <topic> <busline>\n' % sys.argv[0])
        sys.exit(1)

    topic = sys.argv[1]
    busline = sys.argv[2]
    conf = get_config()
    p = Producer(**conf)

    data = {'busline': busline}

    admin_client = AdminClient({'bootstrap.servers': get_config('bootstrap.servers')})
    topics = [topic]
    example_create_topics(admin_client, topics)
    coordinates = get_coordinates()
    for topic in topics:
        generate_checkpoint(coordinates)
