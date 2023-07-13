"""Events are server occurances of different types. Events can happen as a result of
client interactions with the server, or (in future) can be scheduled based upon a
tick timer or cron.

Some Events call Actions directly. Others, like user input, will be ran through the
CommandProcessor to determine which Action should be called.
"""

from cibo.events.__event__ import Event
from cibo.events.connect import Connect
from cibo.events.disconnect import Disconnect
from cibo.events.input import Input

_ = Event, Connect, Disconnect, Input
