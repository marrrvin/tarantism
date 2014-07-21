
from tarantism.errors import DoesNotExist
from tarantism.fields import BaseField
from tarantism.connection import get_space


class ModelManager(object):
    @property
    def space(self):
        return get_space()

    def get(self, key):
        data = self.space.select(key)

        if not data:
            raise DoesNotExist(
                '{klass} instance does not exists.'.format(klass=self.klass)
            )

        return self.klass(data)

    def save(self, data):
        return self.space.insert(tuple(data))

    def delete(self, key):
        return self.space.delete(key)


class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(ModelMetaclass, cls).__new__

        fields = {}
        for attr_name, attr_value in attrs.iteritems():
            if not isinstance(attr_value, BaseField):
                continue

            attr_value.name = attr_name
            fields[attr_name] = attr_value

        attrs['_fields'] = fields

        return super_new(cls, name, bases, attrs)


class Model(object):
    __metaclass__ = ModelMetaclass

    DoesNotExist = DoesNotExist

    objects = ModelManager()

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            if key in self._fields:
                setattr(self, key, value)

        self.objects.klass = self.__class__

        self._data = {}

    def save(self):
        dct = self.__class__.__dict__
        data = []

        return self.objects.save(data)

    def delete(self):
        pk = getattr(self, 'pk')

        return self.objects.delete(pk)
