import pkgutil
import inspect
import sys

OPERATIONS = {}

package = sys.modules[__name__]

for loader, name, is_pkg in pkgutil.iter_modules(package.__path__):
    module = loader.find_module(name).load_module(name)

    for attr_name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj):
            OPERATIONS[attr_name] = obj
