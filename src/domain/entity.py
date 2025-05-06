import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, Optional, Type, TypeVar

T = TypeVar('T', bound='Entity')

class Entity(ABC):
    def __init__(
        self,
        id: Optional[uuid.UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        deleted_at: Optional[datetime] = None,
    ):
        self.id = id if id is not None else uuid.uuid4()
        self.created_at = created_at if created_at is not None else datetime.now()
        self.updated_at = updated_at if updated_at is not None else datetime.now()
        self.deleted_at = deleted_at
        self.is_deleted = True if deleted_at is not None else False

    @abstractmethod
    def validate() -> None:
        pass

    def update(self) -> None:
        self.updated_at = datetime.now()

    def __delete(self) -> None:
        self.deleted_at = datetime.now()
        self.is_deleted = True

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

    def __eq__(self, other) -> bool:
        if not isinstance(other, Entity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
