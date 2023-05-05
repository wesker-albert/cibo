"""Database model"""

from peewee import Model, SqliteDatabase


class DatabaseModel(Model):
    """Base model for inheritance by other DB models"""

    class Meta:
        """Meta class that specifies the database"""

        database = SqliteDatabase("cibo_database.db")
