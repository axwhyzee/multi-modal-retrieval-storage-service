import pytest

from domain.events import DocPersisted, Event


@pytest.mark.parametrize(
    "event,expected",
    ((DocPersisted("user1/test.txt"), "DocPersisted"),),
)
def test_event_channel_equals_class_name(event: Event, expected: str) -> None:
    assert event.channel == expected
