"""Data models and schemas that are used to represent and validate a database object."""

from os import getenv
from typing import Any

from marshmallow import Schema
from peewee import Model as Model_
from peewee import SqliteDatabase


class Model(Model_):
    """Base model for inheritance by other data models."""

    class Meta:
        """Meta class that specifies the database."""

        database = SqliteDatabase(getenv("DATABASE_PATH"))

    def validate(self, schema: type[Schema]) -> Any:
        """Validate the model instance's attributes against the provided schema.

        Args:
            schema (Schema): The marshmallow schema to validate against.
        """

        schema().load(self.__data__)
