
from tarantism.errors import DoesNotExist
from tarantism.fields import Field
from tarantism.backend import spaces
from tarantism.backend import DEFAULT_ALIAS


class ModelManager(object):
    @property
    def space(self):
        return spaces[DEFAULT_ALIAS]

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


class Model(object):
    DoesNotExist = DoesNotExist

    objects = ModelManager()

    def __init__(self, *args, **kwargs):
        dct = self.__class__.__dict__
        for key, value in kwargs.iteritems():
            if key in dct and isinstance(dct[key], Field):
                setattr(self, key, value)

        self.objects.klass = self.__class__

    def save(self):
        dct = self.__class__.__dict__
        data = []

        for key, value in dct.iteritems():
            if key in dct and isinstance(dct[key], Field):
                data.append(getattr(self, key))

        return self.objects.save(data)

    def delete(self):
        pk = getattr(self, 'pk')

        return self.objects.delete(pk)
