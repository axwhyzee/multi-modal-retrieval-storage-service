import json
from abc import ABC, abstractmethod
from dataclasses import asdict

import redis

from config import get_redis_connection_params
from domain.events import Event


class AbstractPublisher(ABC):
    @abstractmethod
    def publish(self, event: Event) -> None: ...


class RedisPublisher(AbstractPublisher):
    def __init__(self):
        self.client = redis.Redis(**get_redis_connection_params())

    def publish(self, event: Event):
        self.client.publish(event.channel, json.dumps(asdict(event)))
