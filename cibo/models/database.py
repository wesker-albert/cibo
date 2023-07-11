"""Database model meta and methods, for inheritance by all database models."""


from marshmallow import Schema
from peewee import Model, SqliteDatabase


class DatabaseModel(Model):
    """Base model for inheritance by other DB models."""

    class Meta:
        """Meta class that specifies the database."""

        database = SqliteDatabase("cibo_database.db")

    def validate(self, schema: type[Schema]):
        """Validate the model instance's attributes against the provided schema.

        Args:
            schema (Schema): The marshmallow schema to validate against
        """

        schema().load(self.__data__)
