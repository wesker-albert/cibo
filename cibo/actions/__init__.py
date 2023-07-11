"""Actions are blocks of logic that are individually processed when a client sends
the server a particular command, associated with that specific Action.

Any newly added Action classes will also need to have a Command() map added to the
`cibo.command.CommandProcessor._commands()` method. Only then will the new Action be
available to clients.
"""

from cibo.actions.__action__ import Action
from cibo.actions.exits import Exits
from cibo.actions.finalize import Finalize
from cibo.actions.login import Login
from cibo.actions.look import Look
from cibo.actions.move import Move
from cibo.actions.quit import Quit
from cibo.actions.register import Register
from cibo.actions.say import Say

_ = Action, Exits, Finalize, Login, Look, Move, Quit, Register, Say
