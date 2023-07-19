"""Actions are blocks of logic that are individually processed when an Event calls
them directly, or a client sends the server a particular Command, associated with that
specific Action.

Any newly added Action classes that will be driven by Command from the client will
need to be added to the ACTIONS list. Only then will the new Action be available to
clients.

Actions that are called directly by an Event should have a filename prefixed with a
singular underscore.
"""

from cibo.actions.close import Close
from cibo.actions.exits import Exits
from cibo.actions.finalize import Finalize
from cibo.actions.login import Login
from cibo.actions.logout import Logout
from cibo.actions.look import Look
from cibo.actions.move import Move
from cibo.actions.open import Open
from cibo.actions.quit import Quit
from cibo.actions.register import Register
from cibo.actions.say import Say

ACTIONS = [
    Close,
    Exits,
    Finalize,
    Login,
    Logout,
    Look,
    Move,
    Open,
    Quit,
    Register,
    Say,
]
