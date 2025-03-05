from io import BytesIO
from typing import Iterator, Type, cast

import pytest
from event_core.adapters.pubsub import FakePublisher
from event_core.domain.events import (
    ChunkStored,
    ChunkThumbnailStored,
    DocStored,
    DocThumbnailStored,
    ObjStored,
)
from event_core.domain.types import UnitType
from flask.testing import FlaskClient

from app import app
from bootstrap import MODULES, DIContainer
from repository import FakeRepository


@pytest.fixture
def key() -> str:
    return "user1/test.txt"


@pytest.fixture
def data() -> bytes:
    return b"test_content"


@pytest.fixture
def api_client() -> Iterator[FlaskClient]:
    with app.test_client() as client:
        yield client


@pytest.fixture
def container() -> DIContainer:
    container = DIContainer()
    container.repo.override(FakeRepository())
    container.pub.override(FakePublisher())
    container.wire(modules=MODULES)
    return container


def test_get_endpoint(
    key: str, data: bytes, api_client: FlaskClient, container: DIContainer
) -> None:
    repo = container.repo()
    repo[key] = data
    response = api_client.get(f"/get/{key}")
    assert response.status_code == 200
    assert response.data == data


@pytest.mark.parametrize(
    "unit_type,expected_event_type",
    (
        (UnitType.CHUNK, ChunkStored),
        (UnitType.CHUNK_THUMBNAIL, ChunkThumbnailStored),
        (UnitType.DOC, DocStored),
        (UnitType.DOC_THUMBNAIL, DocThumbnailStored),
    ),
)
def test_adds_object_to_repo_and_publish_event(
    key: str,
    data: bytes,
    container: DIContainer,
    api_client: FlaskClient,
    unit_type: UnitType,
    expected_event_type: Type[ObjStored],
) -> None:
    form_data = {
        "file": (BytesIO(data), key),
        "key": key,
        "type": unit_type,
    }
    response = api_client.post(
        "/add", data=form_data, content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert container.repo()[key] == data

    pub = cast(FakePublisher, container.pub())
    assert pub._published == [expected_event_type(key=key)]
