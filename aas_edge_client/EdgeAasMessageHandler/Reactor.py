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

    def register_handler(self, event_name, handler):
        """Register a message handler for a specific event."""
        # should we have a check if is this child class of EventHandler?
        handlers = self.handlers.get(event_name, []) # If no handlder for this event, return empty list
        if not handler in handlers: # if empty -> add to list
            handlers.append(handler)
            self.handlers[event_name] = handlers # -> there will be only 1 element in the list [handler] -> should it be a list?

    def unregister_handler(self, event_name, handler):
        """Unregister a message handler for a specific event."""
        handlers = self.handlers.get(event_name, [])
        if handler in handlers: # if empty -> do nothing, if handler not in handlers -> do nothing
            handlers.remove(handler) # if list is empty -> lead to error if remove -> need check
        
    def handle_event(self, event_name, *args, **kwargs):
        """Dispatch the event to the appropriate handler."""
        print("Reactor.handle_event() called \n event_name: {} \n args: {} \n kwargs: {}".format(event_name, args, kwargs))
        handlers = self.handlers.get(event_name, [])
        if handlers.__len__() == 0:
            print("No handlers registered for event: {}".format(event_name))
        for handler in handlers:
            handler.handle_event(*args, **kwargs)