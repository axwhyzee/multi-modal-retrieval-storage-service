from dataclasses import dataclass


@dataclass
class Event:
    def __post_init__(self):
        self.channel = self.__class__.__name__

@dataclass
class DocPersisted(Event):
    doc_id: str
