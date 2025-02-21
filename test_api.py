from io import BytesIO
from typing import Iterator
from unittest.mock import patch

import pytest
from event_core.conftest import FakeRepository  # type: ignore
from flask.testing import FlaskClient

from app import app


@pytest.fixture
def obj_id() -> str:
    return "user1/test.txt"


@pytest.fixture
def obj_data() -> bytes:
    return b"test_content"


@pytest.fixture
def api_client() -> Iterator[FlaskClient]:
    with app.test_client() as client:
        yield client


def test_get_endpoint(
    obj_id: str, obj_data: bytes, api_client: FlaskClient
) -> None:
    with patch("app.repo", FakeRepository()) as repo:
        repo.add(obj_data, obj_id)
        response = api_client.get(f"/get/{obj_id}")
    assert response.status_code == 200
    assert response.data == obj_data


def test_add_endpoint(
    obj_id: str, obj_data: bytes, api_client: FlaskClient
) -> None:
    data = {"file": (BytesIO(obj_data), obj_id), "key": obj_id}
    with patch("app.repo", FakeRepository()) as repo:
        response = api_client.post(
            "/add", data=data, content_type="multipart/form-data"
        )
        assert repo.get(obj_id) == obj_data
    assert response.status_code == 200
