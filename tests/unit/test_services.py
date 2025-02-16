from adapters.repository import AbstractRepository
from conftest import FakePublisher, FakeRepository
from domain.events import DocPersisted
from service_layer.services import add_doc, get_doc


def test_add_doc(
    doc_id: str,
    doc_bytes: bytes,
    fake_repo: AbstractRepository,
    fake_publisher: FakePublisher,
) -> None:
    add_doc(doc_id, doc_bytes, fake_repo, fake_publisher)
    assert fake_repo.get(doc_id) == doc_bytes
    assert fake_publisher.published[0] == DocPersisted(doc_id)


def test_get_doc(doc_id: str, doc_bytes: bytes, fake_repo: FakeRepository) -> None:
    fake_repo._docs = {doc_id: doc_bytes}
    assert get_doc(doc_id, fake_repo) == doc_bytes
