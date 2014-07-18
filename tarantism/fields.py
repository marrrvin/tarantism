
class Field(object):
    def db_type(self, value):
        return value

    def __init__(self):
        self.value = None

    def __get__(self, obj, type=None):
        return self.value

    def __set__(self, obj, value):
        self.value = self.db_type(value)


class NumField(Field):
    def db_type(self, value):
        return int(value)


class Num64Field(Field):
    def db_type(self, value):
        return long(value)


class StrField(Field):
    def db_type(self, value):
        return str(value)
