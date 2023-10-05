from EventHandler import EventHandler

# Handler base class for handling messages from the AAS Edge Client
class TwinEventHandler(EventHandler):

    def handle_message(self, *args, **kwargs):
        return super().handle_event(*args, **kwargs)