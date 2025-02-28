from typing import Dict, Type

from event_core.adapters.pubsub import RedisPublisher
from event_core.config import get_deployment_env
from event_core.domain.events import (
    ChunkStored,
    ChunkThumbnailStored,
    DocStored,
    DocThumbnailStored,
    ObjStored,
)
from event_core.domain.types import Modal, ObjectType

from repository import LocalRepository, S3Repository

repo = LocalRepository() if get_deployment_env() == "DEV" else S3Repository()
pub = RedisPublisher()

EVENTS: Dict[str, Type[ObjStored]] = {
    ObjectType.CHUNK: ChunkStored,
    ObjectType.CHUNK_THUMBNAIL: ChunkThumbnailStored,
    ObjectType.DOC: DocStored,
    ObjectType.DOC_THUMBNAIL: DocThumbnailStored,
}


def handle_add(data: bytes, key: str, obj_type: str, modal: Modal):
    repo.add(data, key)
    event = EVENTS[obj_type](key=key, modal=modal)
    pub.publish(event)


def handle_get(key: str) -> bytes:
    return repo.get(key)


def handle_delete(key: str) -> None:
    repo.delete(key)
