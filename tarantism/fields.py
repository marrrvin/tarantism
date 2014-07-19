
class BaseField(object):
    name = None

    def db_type(self, value):
        return value

    def __init__(self, required=False, default=None):
        self.required = required
        self.default = default

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return instance._data.get(self.name)

    def __set__(self, instance, value):
        if value is None and self.default is not None:
            value = self.default

        instance._data[self.name] = value


class NumField(BaseField):
    def db_type(self, value):
        return int(value)


class Num64Field(BaseField):
    def db_type(self, value):
        return long(value)


class StrField(BaseField):
    def db_type(self, value):
        return str(value)
