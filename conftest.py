from typing import Dict, Iterator

import pytest
from flask.testing import FlaskClient

from adapters.repository import AbstractRepository
from app import app


class FakeRepository(AbstractRepository):
    def __init__(self):
        self._docs: Dict[str, bytes] = {}

    def add(self, doc_id: str, doc_bytes: bytes) -> None:
        self._docs[doc_id] = doc_bytes

    def delete(self, doc_id: str) -> None:
        self._docs.pop(doc_id)

    def get(self, doc_id: str) -> bytes:
        return self._docs[doc_id]


@pytest.fixture
def fake_repo() -> AbstractRepository:
    return FakeRepository()


@pytest.fixture
def api_client() -> Iterator[FlaskClient]:
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def doc_id() -> str:
    return "user1/test.txt"


@pytest.fixture
def doc_bytes() -> bytes:
    return b"test content"
