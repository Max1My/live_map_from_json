import configparser
import socket


def get_config(key: str | None = None):
    config = {'bootstrap.servers': 'localhost:9092',
              'client.id': socket.gethostname(),
              'session.timeout.ms': 6000,
              'auto.offset.reset': 'earliest', 'enable.auto.offset.store': False,
              'group.id': socket.gethostname()
              }
    if key:
        return config[key]
    return config


sr_config = {
    'url': 'http://localhost:9092',
    'basic.auth.user.info': 'WEOJkoneqw213:oinweroijqwe'
}
