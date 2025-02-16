from adapters.event_publisher import AbstractPublisher
from adapters.repository import AbstractRepository
from domain.events import DocPersisted


def add_doc(
    doc_id: str,
    doc_bytes: bytes,
    repo: AbstractRepository,
    publisher: AbstractPublisher,
) -> None:
    repo.add(doc_id, doc_bytes)
    publisher.publish(DocPersisted(doc_id))


def get_doc(doc_id: str, repo: AbstractRepository) -> bytes:
    return repo.get(doc_id)
