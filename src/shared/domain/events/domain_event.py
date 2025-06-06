import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from src.shared.domain.core import Aggregate

class DomainEvent(ABC):
    def __init__(self, aggregate: "Aggregate"):
        self.event_id = str(uuid.uuid4())
        self.occurred_on = datetime.now()
        self.aggregate_id = aggregate.id
        self.event_data = aggregate
        self.version = 1
    
    @property
    def event_type(self) -> str:
        return self.__class__.__name__
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "aggregate_id": self.aggregate_id,
            "event_data": self.event_data.to_dict(),
            "occurred_on": self.occurred_on.isoformat(),
            "version": self.version
        }
    
    @abstractmethod  
    def __repr__(self) -> str:
        pass 