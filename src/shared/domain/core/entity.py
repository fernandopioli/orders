import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, Type, TypeVar, List


T = TypeVar('T', bound='Entity')

class Entity(ABC):
    def __init__(
        self,
        id: uuid.UUID | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        deleted_at: datetime | None = None,
    ):
        self.id = id if id is not None else uuid.uuid4()
        self.created_at = created_at if created_at is not None else datetime.now()
        self.updated_at = updated_at if updated_at is not None else datetime.now()
        self.deleted_at = deleted_at
        self.is_deleted = True if deleted_at is not None else False
        

    def update(self) -> None:
        self.updated_at = datetime.now()

    def delete(self) -> None:
        self.deleted_at = datetime.now()
        self.is_deleted = True

    def __eq__(self, other) -> bool:
        if not isinstance(other, Entity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    @staticmethod
    @abstractmethod
    def validate(*args) -> None:
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": str(self.id),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
        }
    
    @classmethod
    @abstractmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        pass


