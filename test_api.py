from io import BytesIO
from typing import Type
from unittest.mock import patch

import pytest
from event_core.domain.events import (
    ChunkStored,
    ChunkThumbnailStored,
    DocStored,
    DocThumbnailStored,
    ObjStored,
)
from event_core.domain.types import ObjectType
from flask.testing import FlaskClient

from conftest import FakePublisher, FakeRepository


def test_get_endpoint(
    obj_path: str, obj_data: bytes, api_client: FlaskClient
) -> None:
    with patch("services.handlers.repo", FakeRepository()) as repo:
        repo.add(obj_data, obj_path)
        response = api_client.get(f"/get/{obj_path}")
    assert response.status_code == 200
    assert response.data == obj_data


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
    obj_path: str,
    obj_data: bytes,
    api_client: FlaskClient,
    obj_type: ObjectType,
    expected_event_type: Type[ObjStored],
) -> None:
    data = {
        "file": (BytesIO(obj_data), obj_path),
        "key": obj_path,
        "obj_type": obj_type,
    }
    with patch("services.handlers.repo", FakeRepository()) as repo, patch(
        "services.handlers.pub", FakePublisher()
    ) as pub:
        response = api_client.post(
            "/add", data=data, content_type="multipart/form-data"
        )
        assert repo.get(obj_path) == obj_data
        assert pub._published == [expected_event_type(obj_path=obj_path)]
    assert response.status_code == 200
