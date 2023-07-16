"""Data model meta and methods, for inheritance by all data models."""

import os

from dotenv import load_dotenv
from marshmallow import Schema
from peewee import Model as Model_
from peewee import SqliteDatabase
from playhouse.shortcuts import model_to_dict


class Model(Model_):
    """Base model for inheritance by other data models."""

    class Meta:
        """Meta class that specifies the database."""

        load_dotenv()

        database = SqliteDatabase(os.getenv("DATABASE_PATH", "cibo_database.db"))

    def asdict(self) -> dict:
        """Converts the peewee model into a dict representation.

        Returns:
            dict: The model in dict format.
        """

        return model_to_dict(self)

    def validate(self, schema: type[Schema]):
        """Validate the model instance's attributes against the provided schema.

        Args:
            schema (Schema): The marshmallow schema to validate against
        """

        schema().load(self.__data__)
