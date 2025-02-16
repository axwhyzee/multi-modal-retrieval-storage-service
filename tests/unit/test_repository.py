import pytest

from adapters.repository import AbstractRepository


def test_add_and_get_doc(
    fake_repo: AbstractRepository, doc_id: str, doc_bytes: bytes
) -> None:
    fake_repo.add(doc_id, doc_bytes)
    assert fake_repo.get(doc_id) == doc_bytes


def test_del_non_existent_doc(
    fake_repo: AbstractRepository, doc_id: str, doc_bytes: bytes
) -> None:
    fake_repo.add(doc_id, doc_bytes)
    fake_repo.delete(doc_id)
    with pytest.raises(KeyError) as e:
        fake_repo.delete(doc_id)
