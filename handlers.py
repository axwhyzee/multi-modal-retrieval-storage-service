from typing import Dict, List, Tuple, Type, TypeAlias

from dependency_injector.wiring import Provide, inject
from event_core.adapters.pubsub import AbstractPublisher
from event_core.domain.events.base import (
    DocStored,
    DocThumbnailStored,
    ElementThumbnailStored,
    ObjStored,
)
from event_core.domain.events.elements import (
    CodeElementStored,
    ImageElementStored,
    PlotElementStored,
    TextElementStored,
)
from event_core.domain.types import Asset, Element

from bootstrap import DIContainer
from repository import AbstractRepository

EventT: TypeAlias = Type[ObjStored]
RepoObjectT: TypeAlias = str

EVENTS: Dict[RepoObjectT, EventT] = {
    Asset.DOC: DocStored,
    Asset.DOC_THUMBNAIL: DocThumbnailStored,
    Asset.ELEM_THUMBNAIL: ElementThumbnailStored,
    Element.IMAGE: ImageElementStored,
    Element.PLOT: PlotElementStored,
    Element.TEXT: TextElementStored,
    Element.CODE: CodeElementStored,
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
