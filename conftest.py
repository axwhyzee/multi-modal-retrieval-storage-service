from typing import Dict, Iterator

import pytest
from event_core.adapters.pubsub import AbstractPublisher
from event_core.adapters.services.exceptions import ObjectNotExists
from event_core.domain.events import Event
from flask.testing import FlaskClient

from adapters.repository import AbstractRepository
from app import app


class FakeRepository(AbstractRepository):
    def __init__(self):
        self._docs: Dict[str, bytes] = {}

    def add(self, data: bytes, key: str) -> None:
        self._docs[key] = data

    def delete(self, key: str) -> None:
        if key not in self._docs:
            raise ObjectNotExists
        self._docs.pop(key)

    def get(self, key: str) -> bytes:
        if key not in self._docs:
            raise ObjectNotExists
        return self._docs[key]


class FakePublisher(AbstractPublisher):
    def __init__(self):
        self._published = []

    def publish(self, event: Event) -> None:
        self._published.append(event)

    def __exit__(self, *_): ...


@pytest.fixture
def obj_path() -> str:
    return "user1/test.txt"


@pytest.fixture
def obj_data() -> bytes:
    return b"test_content"


@pytest.fixture
def api_client() -> Iterator[FlaskClient]:
    with app.test_client() as client:
        yield client
