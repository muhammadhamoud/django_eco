import uuid
from django.db import models

class UUIDAutoField(models.AutoField):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.postgresql':
            return 'uuid'
        return 'char(32)'

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        if isinstance(value, int):
            value = str(value)
        try:
            return uuid.UUID(value)
        except ValueError:
            raise ValueError(f'{value} is not a valid UUID')

    def to_python(self, value):
        if isinstance(value, uuid.UUID):
            return value
        if value is None:
            return value
        return uuid.UUID(value)

    def get_prep_value(self, value):
        if value is None:
            return None
        return str(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return None
        if isinstance(value, uuid.UUID):
            value = str(value)
        return value

    def get_internal_type(self):
        return 'UUIDAutoField'
