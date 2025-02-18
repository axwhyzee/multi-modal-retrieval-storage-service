from io import BytesIO
from unittest.mock import patch

from flask.testing import FlaskClient

from conftest import FakeRepository


def test_get_endpoint(doc_id: str, doc_bytes: bytes, api_client: FlaskClient) -> None:
    with patch("app.repo", FakeRepository()) as repo:
        repo.add(doc_id, doc_bytes)
        response = api_client.get(f"/get/{doc_id}")
    assert response.status_code == 200
    assert response.data == doc_bytes


def test_add_endpoint(doc_id: str, doc_bytes: bytes, api_client: FlaskClient) -> None:
    data = {"file": (BytesIO(doc_bytes), doc_id), "doc_id": doc_id}
    with patch("app.repo", FakeRepository()) as repo:
        response = api_client.post(
            "/add", data=data, content_type="multipart/form-data"
        )
        assert repo.get(doc_id) == doc_bytes
    assert response.status_code == 200
