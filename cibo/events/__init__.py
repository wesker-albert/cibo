"""Events are server occurances of different types. Events can happen as a result of
client interactions with the server, or (in future) can be scheduled based upon a
tick timer or cron.

Some events call actions directly. Others, like user input, will be ran through the
CommandProcessor to determine which action should be called.
"""

from cibo.events.connect import ConnectEvent
from cibo.events.disconnect import DisconnectEvent
from cibo.events.input import InputEvent
from cibo.events.spawn import SpawnEvent
from cibo.events.tick import TickEvent
