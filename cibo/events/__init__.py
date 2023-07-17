"""Events are server occurances of different types. Events can happen as a result of
client interactions with the server, or (in future) can be scheduled based upon a
tick timer or cron.

Some Events call Actions directly. Others, like user input, will be ran through the
CommandProcessor to determine which Action should be called.
"""
