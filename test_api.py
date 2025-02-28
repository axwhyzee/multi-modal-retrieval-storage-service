from io import BytesIO
from typing import Dict, Iterator, Type
from unittest.mock import patch

import pytest
from event_core.adapters.pubsub import AbstractPublisher
from event_core.adapters.services.exceptions import ObjectNotExists
from event_core.domain.events import (
    ChunkStored,
    ChunkThumbnailStored,
    DocStored,
    DocThumbnailStored,
    Event,
    ObjStored,
)
from event_core.domain.types import Modal, ObjectType
from flask.testing import FlaskClient

from app import app
from repository import AbstractRepository


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
def key() -> str:
    return "user1/test.txt"


@pytest.fixture
def data() -> bytes:
    return b"test_content"


@pytest.fixture
def modal() -> Modal:
    return Modal.TEXT


@pytest.fixture
def api_client() -> Iterator[FlaskClient]:
    with app.test_client() as client:
        yield client


def test_get_endpoint(key: str, data: bytes, api_client: FlaskClient) -> None:
    with patch("handlers.repo", FakeRepository()) as repo:
        repo.add(data, key)
        response = api_client.get(f"/get/{key}")
    assert response.status_code == 200
    assert response.data == data


@pytest.mark.parametrize(
    "obj_type,expected_event_type",
    (
        (ObjectType.CHUNK, ChunkStored),
        (ObjectType.CHUNK_THUMBNAIL, ChunkThumbnailStored),
        (ObjectType.DOC, DocStored),
        (ObjectType.DOC_THUMBNAIL, DocThumbnailStored),
    ),
)
def test_adds_object_to_repo_and_publish_event(
    key: str,
    data: bytes,
    modal: Modal,
    api_client: FlaskClient,
    obj_type: ObjectType,
    expected_event_type: Type[ObjStored],
) -> None:
    form_data = {
        "file": (BytesIO(data), key),
        "key": key,
        "obj_type": obj_type,
        "modal": Modal.TEXT,
    }
    with patch("handlers.repo", FakeRepository()) as repo, patch(
        "handlers.pub", FakePublisher()
    ) as pub:
        response = api_client.post(
            "/add", data=form_data, content_type="multipart/form-data"
        )
        assert response.status_code == 200
        assert repo.get(key) == data
        assert pub._published == [
            expected_event_type(key=key, modal=Modal.TEXT)
        ]
    assert response.status_code == 200
