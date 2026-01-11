import threading
from collections import defaultdict

class MemoryStore:
    def __init__(self):
        self._data = defaultdict(dict)
        self._lock = threading.RLock()

    def set_value(self, namespace, key, value):
        with self._lock:
            self._data[namespace][key] = value

    def get_value(self, namespace, key, default=None):
        with self._lock:
            return self._data[namespace].get(key, default)

    def get_namespace(self, namespace):
        with self._lock:
            return dict(self._data[namespace]) 

    def remove_value(self, namespace, key):
        with self._lock:
            self._data[namespace].pop(key, None)

    def clear_namespace(self, namespace):
        with self._lock:
            self._data[namespace].clear()

    def clear_all(self):
        with self._lock:
            self._data.clear()


store = MemoryStore()
