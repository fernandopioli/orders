from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from src.shared.domain.core.aggregate import Aggregate

class DomainEvent(ABC):
    def __init__(self, entity: "Aggregate"):
        self.occurred_on = datetime.now()
        self.event_data = entity
    
    @property
    def event_type(self) -> str:
        return self.__class__.__name__
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_type": self.event_type,
            "occurred_on": self.occurred_on.isoformat(),
            "event_data": self.event_data.to_dict()
        }
    
    @abstractmethod  
    def __repr__(self) -> str:
        pass 