"""Data model meta and methods, for inheritance by all data models."""

import os
from typing import Any

from dotenv import load_dotenv
from marshmallow import Schema
from peewee import Model as Model_
from peewee import SqliteDatabase


class Model(Model_):
    """Base model for inheritance by other data models."""

    class Meta:
        """Meta class that specifies the database."""

        load_dotenv()

        database = SqliteDatabase(os.getenv("DATABASE_PATH", "cibo_database.db"))

    def validate(self, schema: type[Schema]) -> Any:
        """Validate the model instance's attributes against the provided schema.

        Args:
            schema (Schema): The marshmallow schema to validate against.
        """

        schema().load(self.__data__)
