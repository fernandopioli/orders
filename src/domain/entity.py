import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional


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
    def validate(self) -> None:
        pass

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
