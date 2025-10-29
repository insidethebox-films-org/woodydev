class EventBus:
    
    def __init__(self):
        self.listeners = {}
    
    def subscribe(self, event_name, callback):
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        
        self.listeners[event_name].append(callback)
        
    def publish(self, event_name, data=None):
        if event_name in self.listeners:
            for callback in self.listeners[event_name]:
                try:
                    callback(data)
                except Exception as e:
                    callback_name = f"{callback.__self__.__class__.__name__}.{callback.__name__}" if hasattr(callback, '__self__') else callback.__name__
                    print(f"Error in {callback_name} callback for '{event_name}': {e}")
                    
                    import traceback
                    traceback.print_exc()

event_bus = EventBus()