
from tarantism.metaclasses import ModelMetaclass
from tarantism.connection import get_space
from tarantism.connection import DEFAULT_ALIAS
from tarantism.errors import ValidationError


__all__ = ['Model']


class Model(object):
    __metaclass__ = ModelMetaclass

    def __init__(self, **kwargs):
        self._data = {}

        # Set defaults
        for key, field in self._fields.iteritems():
            value = getattr(self, key, None)
            setattr(self, key, value)

        for key, value in kwargs.iteritems():
            if key in self._fields:
                setattr(self, key, value)

    @classmethod
    def _get_space(cls):
        return get_space(
            cls._meta.get('db_alias', DEFAULT_ALIAS)
        )

    def validate(self):
        for field_name, field in self._fields.items():
            value = self._data.get(field_name)
            if value is not None:
                field.validate(value)

            elif field.required:
                raise ValidationError('Field {name} is required.'.format(name=field.name))

    def to_db(self):
        data = {}
        for field_name, field in self._fields.items():
            value = self._data.get(field_name, None)
            data[field_name] = field.to_db(value)

        return data

    def save(self, validate=True):
        if validate:
            self.validate()

        data = self.to_db()

        self.insert(data)

        return self

    def insert(self, data):
        values = self._dict_to_values(data)

        return self._get_space().insert(values)

    def update(self, **kwargs):
        primary_key_value = self._get_primary_key_value()
        data = self._dict_to_values(kwargs)

        return self._get_space().update(primary_key_value, data)

    def delete(self):
        primary_key_value = self._get_primary_key_value()

        return self._get_space().delete(primary_key_value)

    @classmethod
    def _values_to_dict(cls, values):
        return dict(zip(
            cls._fields_ordered, values
        ))

    @classmethod
    def _dict_to_values(cls, data):
        return tuple([
            data[field_name] for field_name in cls._fields_ordered
        ])

    def _get_primary_key_value(self):
        pk = getattr(self, 'pk', None)
        if pk:
            return pk

        for field_name, field in self._fields.iteritems():
            if field.primary_key:
                return getattr(self, field_name)

        raise ValueError(
            'Model should have primary key field.'
        )
