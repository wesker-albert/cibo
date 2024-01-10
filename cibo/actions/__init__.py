"""Actions are blocks of logic that are individually processed when an event calls
them directly, or a client sends the server a particular command, associated with that
specific action.

Any newly added Action classes that will be driven by a command from the client will
need to have their files created in the `cibo.actions.commands` path. Only then will
the new action be available to clients.
"""

from cibo.actions.connect import Connect
from cibo.actions.disconnect import Disconnect
from cibo.actions.error import Error
