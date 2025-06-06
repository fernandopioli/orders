from datetime import datetime
from src.shared.domain.core import Result
from src.shared.domain.events import DomainEvent, EventPublisher


class ConsoleEventPublisher(EventPublisher):
    
    def publish(self, event: DomainEvent, topic: str) -> Result[None]:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 📤 Publishing event to topic '{topic}'")
        print(f"  Event Type: {event.event_type}")
        print(f"  Event Data: {event.event_data}")
        print(f"  Occurred On: {event.occurred_on}")
        print("  " + "-" * 50)
        
        return Result.ok() 