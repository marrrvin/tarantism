
from tarantism.managers import Manager
from tarantism.metaclasses import ModelMetaclass
from tarantism.connection import get_space
from tarantism.connection import DEFAULT_ALIAS
from tarantism.errors import ValidationError


__all__ = ['Model']


class Model(object):
    __metaclass__ = ModelMetaclass

    objects = Manager()

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
        return get_space(cls._meta.get('db_alias', DEFAULT_ALIAS))

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

        # FIXME
        self.objects.klass = self.__class__
        self.objects.space = self._get_space()

        self.objects.save(data)

        return self

    def delete(self):
        self.objects.klass = self.__class__
        self.objects.space = self._get_space()

        return self.objects.delete(self._get_pk())

    def update(self, **kwargs):
        """
        TODO
        """

    def _get_pk(self):
        pk = getattr(self, 'pk', None)
        if pk:
            return pk

        for field in self._fields.iteritems():
            if field.primary_key:
                return field.primary_key
