
from tarantism.managers import Manager
from tarantism.metaclasses import ModelMetaclass
from tarantism.connection import get_space
from tarantism.connection import DEFAULT_ALIAS


__all__ = ['Model']


class Model(object):
    __metaclass__ = ModelMetaclass

    objects = Manager()

    def __init__(self, **kwargs):
        self._data = {}

        for key, value in kwargs.iteritems():
            if key in self._fields:
                setattr(self, key, value)

    @classmethod
    def _get_space(cls):
        return get_space(cls._meta.get('db_alias', DEFAULT_ALIAS))

    """
    def __iter__(self):

    def __delattr__(self, *args, **kwargs):

    def __setattr__(self, name, value):

    def __getstate__(self):

    def __setstate__(self, data):

    """

    def validate(self):
        for field_name, field in self._fields.items():
            value = self._data.get(field_name)
            if value is not None:
                field.validate(value)

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
        pk = getattr(self, 'pk')

        self.objects.klass = self.__class__
        self.objects.space = self._get_space()

        return self.objects.delete(pk)

    def update(self, **kwargs):
        """
        TODO
        """
