from abc import ABC, abstractmethod
from typing import List

class EventHandler(ABC):
    @abstractmethod
    def handle_event(self, *args, **kwargs):
        pass