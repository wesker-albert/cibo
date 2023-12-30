"""Actions that are called by commands that are made by the client."""


from cibo.actions.commands.close import Close
from cibo.actions.commands.drop import Drop
from cibo.actions.commands.exits import Exits
from cibo.actions.commands.finalize import Finalize
from cibo.actions.commands.get import Get
from cibo.actions.commands.inventory import Inventory
from cibo.actions.commands.login import Login
from cibo.actions.commands.logout import Logout
from cibo.actions.commands.look import Look
from cibo.actions.commands.move import Move
from cibo.actions.commands.open import Open
from cibo.actions.commands.quit import Quit
from cibo.actions.commands.register import Register
from cibo.actions.commands.say import Say

ACTIONS = [
    Close,
    Drop,
    Exits,
    Finalize,
    Get,
    Inventory,
    Login,
    Logout,
    Look,
    Move,
    Open,
    Quit,
    Register,
    Say,
]
