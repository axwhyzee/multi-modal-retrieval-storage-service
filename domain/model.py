from dataclasses import dataclass
from typing import Any, Dict, TypeAlias


DocID: TypeAlias = str


@dataclass
class Document:
    id: DocID
    meta: Dict[str, Any]
