from typing import Dict, Type, List

from dependency_injector.wiring import Provide, inject
from event_core.adapters.pubsub import AbstractPublisher
from event_core.domain.events import (
    ChunkStored,
    ChunkThumbnailStored,
    DocStored,
    DocThumbnailStored,
    ObjStored,
)
from event_core.domain.types import Modal, ObjectType

from bootstrap import DIContainer
from repository import AbstractRepository

EVENTS: Dict[str, Type[ObjStored]] = {
    ObjectType.CHUNK: ChunkStored,
    ObjectType.CHUNK_THUMBNAIL: ChunkThumbnailStored,
    ObjectType.DOC: DocStored,
    ObjectType.DOC_THUMBNAIL: DocThumbnailStored,
}


@inject
def handle_add(
    data: bytes,
    key: str,
    obj_type: str,
    modal: Modal,
    repo: AbstractRepository = Provide[DIContainer.repo],
    pub: AbstractPublisher = Provide[DIContainer.pub],
):
    repo[key] = data
    event = EVENTS[obj_type](key=key, modal=modal)
    pub.publish(event)


@inject
def handle_get(
    key: str, repo: AbstractRepository = Provide[DIContainer.repo]
) -> bytes:
    return repo[key]


@inject
def handle_delete(
    key: str, repo: AbstractRepository = Provide[DIContainer.repo]
) -> None:
    del repo[key]


@inject
def handle_len(repo: AbstractRepository = Provide[DIContainer.repo]) -> int:
    return len(repo)


@inject
def handle_list(repo: AbstractRepository = Provide[DIContainer.repo]) -> List[str]:
    return list(repo)
