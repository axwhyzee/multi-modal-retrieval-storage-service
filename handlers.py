from typing import Dict, Type

from event_core.adapters.pubsub import RedisPublisher
from event_core.domain.events import (
    ChunkStored,
    ChunkThumbnailStored,
    DocStored,
    DocThumbnailStored,
    ObjStored,
)
from event_core.domain.types import ObjectType

from repository import S3Repository

repo = S3Repository()
pub = RedisPublisher()

EVENTS: Dict[str, Type[ObjStored]] = {
    ObjectType.CHUNK: ChunkStored,
    ObjectType.CHUNK_THUMBNAIL: ChunkThumbnailStored,
    ObjectType.DOC: DocStored,
    ObjectType.DOC_THUMBNAIL: DocThumbnailStored,
}


def handle_add(data: bytes, key: str, obj_type: str):
    repo.add(data, key)
    event = EVENTS[obj_type](obj_path=key)
    pub.publish(event)


def handle_get(key: str) -> bytes:
    return repo.get(key)


def handle_delete(key: str) -> None:
    repo.delete(key)
