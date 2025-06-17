from src.shared.domain.events import DomainEvent, DomainEventHandler


class ConsoleLogHandler(DomainEventHandler):
    def handle(self, event: DomainEvent) -> None:
        print(f"********************* Event: {event.to_dict()} *********************")
