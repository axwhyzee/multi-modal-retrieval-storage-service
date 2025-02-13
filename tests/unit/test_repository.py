from typing import Dict

import pytest

from adapters.repository import AbstractRepository, DocPayload
from domain.model import DocID


class FakeRepository(AbstractRepository):
    def __init__(self):
        self._docs: Dict[str, DocPayload] = {}

    def add(self, doc_id: DocID, doc_payload: DocPayload) -> None:
        if doc_payload.content_type == "binary/octet-stream":
            self._docs[doc_id] = doc_payload
        else:
            raise ValueError(f"Unrecognized content-type {doc_payload.content_type}")

    def delete(self, doc_id: DocID) -> None:
        self._docs.pop(doc_id)

    def get(self, doc_id: DocID) -> DocPayload:
        return self._docs[doc_id]


@pytest.mark.parametrize(
    "doc_id,doc_payload",
    (
        (
            "test_doc.jpg",
            DocPayload(data=bytes([0]), content_type="binary/octet-stream"),
        ),
    ),
)
def test_add_and_get_doc(doc_id: DocID, doc_payload: DocPayload) -> None:
    repo = FakeRepository()
    repo.add(doc_id, doc_payload)
    assert repo.get(doc_id) == doc_payload


@pytest.mark.parametrize(
    "doc_id,doc_payload",
    (
        (
            "test_doc.jpg",
            DocPayload(data=bytes([0]), content_type="binary/octet-stream"),
        ),
    ),
)
def test_del_non_existent_doc(doc_id: DocID, doc_payload: DocPayload) -> None:
    repo = FakeRepository()
    repo.add(doc_id, doc_payload)
    repo.delete(doc_id)
    with pytest.raises(Exception) as e:
        repo.delete(doc_id)
