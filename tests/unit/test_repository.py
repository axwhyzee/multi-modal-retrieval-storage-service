import pytest

from adapters.repository import AbstractRepository
from conftest import FakeRepository


def test_add_doc(
    fake_repo: FakeRepository, doc_id: str, doc_bytes: bytes
) -> None:
    fake_repo.add(doc_id, doc_bytes)
    assert fake_repo._docs[doc_id] == doc_bytes


def test_get_doc(
    fake_repo: FakeRepository, doc_id: str, doc_bytes: bytes
) -> None:
    fake_repo._docs[doc_id] = doc_bytes
    assert fake_repo.get(doc_id) == doc_bytes


def test_delete_doc(
    fake_repo: FakeRepository, doc_id: str, doc_bytes: bytes
) -> None:
    fake_repo._docs[doc_id] = doc_bytes
    fake_repo.delete(doc_id)
    with pytest.raises(KeyError) as e:
        fake_repo.get(doc_id)


def test_add_and_get_doc(
    fake_repo: AbstractRepository, doc_id: str, doc_bytes: bytes
) -> None:
    fake_repo.add(doc_id, doc_bytes)
    assert fake_repo.get(doc_id) == doc_bytes


def test_non_idempotent_delete(
    fake_repo: AbstractRepository, doc_id: str, doc_bytes: bytes
) -> None:
    fake_repo.add(doc_id, doc_bytes)
    fake_repo.delete(doc_id)
    with pytest.raises(KeyError) as e:
        fake_repo.delete(doc_id)


def test_idempotent_add(
    fake_repo: AbstractRepository, doc_id: str, doc_bytes: bytes
) -> None:
    fake_repo.add(doc_id, doc_bytes)
    fake_repo.add(doc_id, doc_bytes)
    assert fake_repo.get(doc_id) == doc_bytes
