from MessageHandler import MessageHandler
from typing import List

# Base Reactor class
class Reactor:
    def __init__(self):
        self.handlers = {}

    def register_handler(self, protocol, handler):
        """Register a message handler for a specific protocol."""
        if not issubclass(handler, MessageHandler):
            raise ValueError("Handler must be a subclass of MessageHandler")
        self.handlers[protocol] = handler()

    def handle_event(self, request, protocol='rest',*args, **kwargs):
        """Dispatch the event to the appropriate handler."""
        handler = self.handlers.get(protocol)
        if not handler:
            raise ValueError(f"No handler found for protocol: {protocol}")
        return handler.handle_message(request, *args, **kwargs)

