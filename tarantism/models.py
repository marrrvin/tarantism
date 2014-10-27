
from tarantism.metaclasses import ModelMetaclass
from tarantism.connection import get_space
from tarantism.connection import DEFAULT_ALIAS
from tarantism.errors import ValidationError
from tarantism.fields import *


__all__ = ['Model']


OPERATIONS_MAP = {
    'add': '+',
    'assign': '=',
    'and': '&',
    'xor': '^',
    'or': '|',
}


class Model(object):
    __metaclass__ = ModelMetaclass

    def __init__(self, **kwargs):
        self._data = {}

        self.set_default_state()

        for key, value in kwargs.iteritems():
            if key in self._fields:
                setattr(self, key, value)

    def __iter__(self):
        return iter(self._fields_ordered)

    def __getitem__(self, name):
        try:
            if name in self._fields_ordered:
                return getattr(self, name)
        except AttributeError:
            pass

        raise KeyError(name)

    def __setitem__(self, name, value):
        if name not in self._fields:
            raise KeyError(name)

        return setattr(self, name, value)

    @classmethod
    def get_space(cls):
        return get_space(
            cls._meta.get('db_alias', DEFAULT_ALIAS)
        )

    @classmethod
    def _model_from_data(cls, raw_data):
        data = {}
        for field_name, field in cls._fields.iteritems():
            if field_name in raw_data:
                data[field_name] = field.to_python(raw_data[field_name])

        return cls(**data)

    def set_default_state(self):
        self._data = {}
        for field_name, field in self._fields.iteritems():
            value = getattr(self, field_name, None)
            setattr(self, field_name, value)

    def to_db(self):
        data = {}
        for field_name, field in self._fields.items():
            value = self._data.get(field_name, None)
            data[field_name] = field.to_db(value)

        return data

    def validate(self):
        for field_name, field in self._fields.items():
            value = self._data.get(field_name)
            if value is not None:
                field.validate(value)

            elif field.required:
                raise ValidationError(
                    'Field {name} is required.'.format(name=field.name)
                )

    def save(self, validate=True):
        if validate:
            self.validate()

        data = self.to_db()

        return self.insert(data)

    def insert(self, data):
        values = self._dict_to_values(data)

        self.get_space().insert(values)

        return self

    def update(self, **kwargs):
        primary_key_value = self._get_primary_key_value()

        changes = self._make_changes_struct(kwargs)

        values = self.get_space().update(
            primary_key_value, changes
        ).pop()

        return self.__class__(**self._values_to_dict(values))

    def delete(self):
        primary_key_value = self._get_primary_key_value()

        values = self.get_space().delete(primary_key_value)

        return self.__class__(**self._values_to_dict(values))

    @classmethod
    def _get_schema_params(cls):
        schema_params = {
            'name': cls.__name__,
            'fields': {},
            'indexes': {}
        }

        for field_number, field_name in enumerate(cls._fields_ordered):
            field = cls._fields[field_name]

            schema_params['fields'][field_number] = {
                'name': field_name,
                'type': field.db_type
            }

            if field.db_index is not None:
                schema_params['indexes'][field.db_index] = {
                    'name': field.name,
                    'fields': [field_number]
                }
            # FIXME: hack for pk
            elif field.name == 'pk':
                schema_params['indexes'][0] = {
                    'name': field.name,
                    'fields': [0]
                }

        return schema_params

    @classmethod
    def _values_to_dict(cls, values):
        return dict(zip(
            cls._fields_ordered, values
        ))

    @classmethod
    def _dict_to_values(cls, data):
        return tuple([
            data[field_name] for field_name in cls._fields_ordered
            if field_name in data
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

    def _parse_fields(self, data):
        field_operation_map = {}

        for key, value in data.iteritems():
            chunks = key.split('__', 1)

            if len(chunks) == 1:
                field_name = chunks[0]
                modificator = 'assign'
            else:
                field_name = chunks[0]
                modificator = chunks[1]

            try:
                operation = OPERATIONS_MAP[modificator]
            except KeyError:
                raise ValueError(
                    'Unknown field modificator {mod}.'.format(mod=modificator)
                )

            field_operation_map[field_name] = (operation, value)

        return field_operation_map

    def _make_changes_struct(self, data):
        field_operation_map = self._parse_fields(data)
        changes = []
        for field_number, field_name in enumerate(self._fields_ordered):
            if field_name in field_operation_map:
                operation, value = field_operation_map[field_name]

                # FIXME: update do not understand unicode strings.
                if isinstance(value, unicode):
                    value = str(value)

                changes.append((field_number, operation, value))

        return changes
