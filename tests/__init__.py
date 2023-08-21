"""An experimental MUD server, written in Python. Object-oriented and event driven."""

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(".env.test"), override=True)
