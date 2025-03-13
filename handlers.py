from typing import Dict, List, Type

from dependency_injector.wiring import Provide, inject
from event_core.adapters.pubsub import AbstractPublisher
from event_core.domain.events import (
    DocStored,
    DocThumbnailStored,
    ElementThumbnailStored,
    ElementStored,
    ObjStored,
)
from event_core.domain.types import Asset, Element

from bootstrap import DIContainer
from repository import AbstractRepository

EVENTS: Dict[str, Type[ObjStored]] = {
    Asset.DOC: DocStored,
    Asset.DOC_THUMBNAIL: DocThumbnailStored,
    Asset.ELEM_THUMBNAIL: ElementThumbnailStored,
    Element.IMAGE: ElementStored,
    Element.PLOT: ElementStored,
    Element.TEXT: ElementStored,
}


@inject
def handle_add(
    data: bytes,
    key: str,
    repo_obj_type: str,
    repo: AbstractRepository = Provide[DIContainer.repo],
    pub: AbstractPublisher = Provide[DIContainer.pub],
):
    repo[key] = data
    event = EVENTS[repo_obj_type](key=key)
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
def handle_list(
    repo: AbstractRepository = Provide[DIContainer.repo],
) -> List[str]:
    return list(repo)
