"""Actions that are called by Commands that are made by the client."""

from glob import glob
from importlib import import_module
from inspect import isclass
from os import path

# this hacky block of code iterates over all the modules in this folder, identifies
# Action classes within the modules, then compiles them into a list. We do this so
# the CommandProcessor knows what Actions it is allowed to process. It also saves
# us from having to maintain a hardcoded list, for better or worse.
command_actions = []
current_dir = path.join(path.dirname(path.abspath(__file__)))

for file in glob(current_dir + "/*.py"):
    name = path.splitext(path.basename(file))[0]
    module = import_module(f"cibo.actions.commands.{name}")

    for member in dir(module):
        handler_class = getattr(module, member)

        if (
            handler_class
            and isclass(handler_class)
            and handler_class.__base__.__name__ == "Action"
            and handler_class.__module__.startswith("cibo.actions.commands.")
        ):
            command_actions.append(handler_class)

ACTIONS = list(set(command_actions))
