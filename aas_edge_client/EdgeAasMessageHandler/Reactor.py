from .MessageHandler import MessageHandler
from typing import List

# Base Reactor class implementing Singleton pattern.
# https://www.geeksforgeeks.org/singleton-pattern-in-python-a-complete-guide/
# 
class Reactor(object):
    # Singleton instance
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Reactor, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.handlers = {}

    def register_handler(self, protocol, handler):
        """Register a message handler for a specific protocol."""
        if not isinstance(handler, MessageHandler):
            raise ValueError("Handler must be a subclass of MessageHandler")
        self.handlers[protocol] = handler

    def handle_event(self, request, protocol='rest',*args, **kwargs):
        """Dispatch the event to the appropriate handler."""
        handler = self.handlers.get(protocol)
        if not handler:
            raise ValueError(f"No handler found for protocol: {protocol}")
        return handler.handle_message(request, *args, **kwargs)

