class EventBus:
    
    def __init__(self):
        self.listeners = {}
    
    def subscribe(self, event_name, callback):
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        
        self.listeners[event_name].append(callback)
        print(f"Subscribed to '{event_name}' event")
    
    def publish(self, event_name, data=None):
        if event_name in self.listeners:
            for callback in self.listeners[event_name]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"Error in event callback: {e}")
        else:
            print(f"No subscribers for '{event_name}' event")

event_bus = EventBus()