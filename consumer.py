from confluent_kafka import Consumer, KafkaException
import sys
import json
import logging
from pprint import pformat

from settings.config import get_config

logger = logging.getLogger('consumer')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))
logger.addHandler(handler)


def stats_cb(stats_json_str):
    stats_json = json.loads(stats_json_str)
    print('\nKAFKA Stats: {}\n'.format(pformat(stats_json)))


def print_usage_and_exit(program_name):
    sys.stderr.write('Usage: %s [options..] <topic1> <topic2> ..\n' % program_name)
    options = '''
 Options:
  -T <intvl>   Enable client statistics at specified interval (ms)
'''
    sys.stderr.write(options)
    sys.exit(1)


def start_consuming(topics: list[str]):
    conf = get_config()
    c = Consumer(conf, logger=logger)

    def print_assignment(consumer, partitions):
        print('Assignment:', partitions)

    c.subscribe(topics, on_assign=print_assignment)

    try:
        while True:
            msg = c.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            else:
                sys.stderr.write('%% %s [%d] at offset %d with key %s:\n' %
                                 (msg.topic(), msg.partition(), msg.offset(),
                                  str(msg.key())))
                c.store_offsets(msg)
                yield 'data:{0}\n\n'.format(msg.value().decode('utf-8'))

    except KeyboardInterrupt:
        sys.stderr.write('%% Aborted by user\n')

    finally:
        c.close()
