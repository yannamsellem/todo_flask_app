from dataclasses import dataclass
from typing import Any


@dataclass
class Entity:
    id: Any = None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return False
        if self.id is None or other.id is None:
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
