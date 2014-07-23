
import re

from tarantism.errors import ValidationError


__all__ = ['BaseField', 'IntField', 'LongField', 'StringField']


class BaseField(object):
    name = None

    def __init__(self, required=False, default=None,
                 primary_key=False, validation=None, verbose_name=None,
                 help_text=None):
        self.required = required
        self.default = default
        self.primary_key = primary_key
        self.validation = validation
        self.verbose_name = verbose_name
        self.help_text = help_text

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return instance._data.get(self.name)

    def __set__(self, instance, value):
        if value is None and self.default is not None:
            value = self.default

        instance._data[self.name] = value

    def to_python(self, value):
        return value

    def to_db(self, value):
        return self.to_python(value)

    def validate(self, value):
        pass


class IntField(BaseField):
    def __init__(self, min_value=None, max_value=None, **kwargs):
        self.min_value = min_value
        self.max_value = max_value

        super(IntField, self).__init__(**kwargs)

    def validate(self, value):
        try:
            value = int(value)
        except ValueError:
            raise ValidationError('%s could not be converted to int' % value)

        if self.min_value is not None and value < self.min_value:
            raise ValidationError('Integer value is too small')

        if self.max_value is not None and value > self.max_value:
            raise ValidationError('Integer value is too large')

    def to_python(self, value):
        return int(value)


class LongField(BaseField):
    def __init__(self, min_value=None, max_value=None, **kwargs):
        self.min_value = min_value
        self.max_value = max_value

        super(LongField, self).__init__(**kwargs)

    def validate(self, value):
        try:
            value = long(value)
        except ValueError:
            raise ValidationError('%s could not be converted to long' % value)

        if self.min_value is not None and value < self.min_value:
            raise ValidationError('Long value is too small')

        if self.max_value is not None and value > self.max_value:
            raise ValidationError('Long value is too large')

    def to_python(self, value):
        return long(value)


class StringField(BaseField):
    def __init__(self, regex=None, max_length=None, min_length=None, **kwargs):
        self.regex = re.compile(regex) if regex else None
        self.max_length = max_length
        self.min_length = min_length

        super(StringField, self).__init__(**kwargs)

    def validate(self, value):
        if not isinstance(value, basestring):
            raise ValidationError('Field {name} error: {class_name} only accepts string values.'.format(
                name=self.name,
                class_name=self.__class__.__name__
            ))

        if self.max_length is not None and len(value) > self.max_length:
            raise ValidationError('Field {name} error: string value is too long.'.format(name=self.name))

        if self.min_length is not None and len(value) < self.min_length:
            raise ValidationError('String value is too short')

        if self.regex is not None and self.regex.match(value) is None:
            raise ValidationError('String value did not match validation regex')

    def to_python(self, value):
        return str(value)
