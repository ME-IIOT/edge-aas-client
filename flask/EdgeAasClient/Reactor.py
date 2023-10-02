from MessageHandler import MessageHandler
from typing import List

# Base Reactor class
class Reactor:
    def __init__(self):
        self.handlers: List[MessageHandler] = []

    def add_handler(self, handler: 'MessageHandler'):
        self.handlers.append(handler)

    def remove_handler(self, handler: 'MessageHandler'):
        self.handlers.remove(handler)

    def handle_events(self):
        for handler in self.handlers:
            handler.handle_event()
