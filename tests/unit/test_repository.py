from typing import Dict

import pytest

from repository import AbstractRepository


class FakeRepository(AbstractRepository):
    def __init__(self):
        self._docs: Dict[str, bytes] = {}

    def add(self, doc_id: str, doc_bytes: bytes) -> None:
        self._docs[doc_id] = doc_bytes

    def delete(self, doc_id: str) -> None:
        self._docs.pop(doc_id)

    def get(self, doc_id: str) -> bytes:
        return self._docs[doc_id]


@pytest.mark.parametrize(
    "doc_id,doc_bytes",
    (
        ("test_doc.jpg", bytes([0])),
    ),
)
def test_add_and_get_doc(doc_id: str, doc_bytes: bytes) -> None:
    repo = FakeRepository()
    repo.add(doc_id, doc_bytes)
    assert repo.get(doc_id) == doc_bytes


@pytest.mark.parametrize(
    "doc_id,doc_bytes",
    (
        ("test_doc.jpg", bytes([0])),
    ),
)
def test_del_non_existent_doc(doc_id: str, doc_bytes: bytes) -> None:
    repo = FakeRepository()
    repo.add(doc_id, doc_bytes)
    repo.delete(doc_id)
    with pytest.raises(Exception) as e:
        repo.delete(doc_id)
