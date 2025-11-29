from abc import ABC, abstractmethod

class DCC(ABC):
    registry = {}

    @classmethod
    def register(cls, name):
        def wrapper(subclass):
            cls.registry[name.lower()] = subclass
            return subclass
        return wrapper

    @abstractmethod
    def open_file(self, root, group, element, scene):
        pass
