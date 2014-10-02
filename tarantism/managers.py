

__all__ = ['Manager']


class Manager(object):
    def get(self, **kwargs):
        values = kwargs.values()
        response = self.space.select(values)
        if not response.rowcount:
            raise self.klass.DoesNotExist(
                '{klass} instance does not exists.'.format(klass=self.klass)
            )

        data = dict(response)

        return self.klass(**data)

    def save(self, data):
        tpl = tuple(data.values())

        return self.space.insert(tpl)

    def delete(self, key):
        return self.space.delete(key)
