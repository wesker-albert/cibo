# CIBO

(SEE-boh)

An experimental MUD server, written in Python. Object-oriented and event driven.

## What is a "MUD"?

* [Wikipedia: Multi-user Dungeon](https://en.wikipedia.org/wiki/Multi-user_dungeon)
* [Medium: What Are They? And How to Play](https://medium.com/@williamson.f93/multi-user-dungeons-muds-what-are-they-and-how-to-play-af3ec0f29f4a)

## Why?

I loved MUDs as a teen. They were like living, breathing choose your own adventure books.

When I first started my career as a software engineer, I knew there was a possibility
that I'd be working in Python, but at that point I had virtually no experience in it.
I needed a learning project that interested me, that I could hack around with and
get a basic feel for the language.

That project ended up being a sloppy bowl of spaghet, that I dubbed "Office Crawler."
It was a very rudimentary MUD server with a map based upon the floorplan of the office
I was working in at the time. It wasn't pretty, and was hardly finished, but it
gave me the toe dip into the pool of Python that I wanted.

Fast forward to now, years later. Cibo is an attempt to pick up what I started with
Office Crawler. But this time it's a new learning project, where I can practice more
advanced architectural designs and patterns that I've learned since, or been curious
about but haven't gotten the professional opportunity to try.

## Current state:

### 2023-07-18
* New commands available: `open`, `close`
* Introduced interactive doors. If you run into a door you can use `open` or `close`
followed by the direction the door is in. For example `open w` or `close west`
* Doors can also be locked. Currently there's no mechanism to unlock them, but that
functionality will arrive soon enough.

### 2023-07-16
* New command available: `quit`
* Server now has the ability to schedule "tick" timers, that are processed with varying
frequency.
* The current player room is persisted every minute, if a disconnection occurs, or when
`quit` and `logout` are used.
* Thanks to the above, when a player reconnects they will spawn in the last room they
occupied.
* Server command `stop` was discovered to be broken, in the sense that once stopped,
the server cannot be `start`ed again without terminating the program and running it
again. This will be fixed later, as it doesn't currently pose a development
complication.

### 2023-07-15
* New commands available: `look, exits, north, south, east, west`
* A small set of sample rooms were created to test navigation.
* Basic player navigation has been implemented, with the exceptions of `up` and `down`.
* "Local" messages have been completed, and now only print to occupants of the room they
were executed within.

### 2023-07-13
* The project can be loaded via Dev Container in VSCode.
* In terminal, `make start` will fire up the server.
* Once fired up, you can control the server. Make sure to `create_db` before trying
to `start` the server.
* Connect via telnet to: `127.0.0.1 51234`
* Currently available commands:  `register, finalize, login, say, logout`