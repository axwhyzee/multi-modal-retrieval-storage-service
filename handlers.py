from typing import Dict, List, Tuple, Type, TypeAlias

from dependency_injector.wiring import Provide, inject
from event_core.adapters.pubsub import AbstractPublisher
from event_core.domain.events import (
    DocStored,
    DocThumbnailStored,
    ElementStored,
    ElementThumbnailStored,
    ImageElementStored,
    ObjStored,
    PlotElementStored,
    TextElementStored,
)
from event_core.domain.types import Asset, Element

from bootstrap import DIContainer
from repository import AbstractRepository

ChannelT: TypeAlias = str
EventT: TypeAlias = Type[ObjStored]
RepoObjectT: TypeAlias = str

PUB_CHANNELS_AND_EVENTS: Dict[RepoObjectT, Tuple[ChannelT, EventT]] = {
    Asset.DOC.value: (DocStored.__name__, DocStored),
    Asset.DOC_THUMBNAIL.value: (DocThumbnailStored.__name__, DocThumbnailStored,),
    Asset.ELEM_THUMBNAIL.value: (ElementThumbnailStored.__name__, ElementThumbnailStored,),
    Element.IMAGE.value: (ElementStored.__name__, ImageElementStored),
    Element.PLOT.value: (ElementStored.__name__, PlotElementStored),
    Element.TEXT.value: (ElementStored.__name__, TextElementStored),
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
    channel, event_cls = PUB_CHANNELS_AND_EVENTS[repo_obj_type]
    event = event_cls(key=key)
    pub.publish(event, channel=channel)


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
