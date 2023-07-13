# CIBO

(SEE-boh)

An experimental MUD server, written in Python. Object-oriented and event driven.

## What is a "MUD"?

* [Wikipedia: Multi-user Dungeon](https://en.wikipedia.org/wiki/Multi-user_dungeon)
* [Medium: What Are They? And How to Play](https://medium.com/@williamson.f93/multi-user-dungeons-muds-what-are-they-and-how-to-play-af3ec0f29f4a)

## Why?

I loved MUDs as a teen. They were live living, breathing choose your own adventure books.

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

### 2023-07-13
* The project can be loaded via Dev Container in VSCode.
* In terminal, `make start` will fire up the server.
* Once fired up, you'll can control the server. Make sure to `create_db` before trying
to `start` the server.
* Connect via telnet to: `127.0.0.1 51234`
* Currently available commands:  `register, finalize, login, say, logout`