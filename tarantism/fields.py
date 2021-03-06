
import re
from datetime import datetime
from decimal import Decimal

from tarantism.exceptions import ValidationError

__all__ = [
    'BaseField',
    'INT32_MIN', 'INT32_MAX', 'Num32Field',
    'INT64_MIN', 'INT64_MAX', 'Num64Field',
    'StringField', 'BytesField',
    'DateTimeField', 'DEFAULT_DATETIME_FORMAT',
    'DecimalField',
]


INT32_MIN = -2147483648

INT32_MAX = +2147483647

INT64_MIN = -9223372036854775808

INT64_MAX = +9223372036854775807


class BaseField(object):
    name = None

    # Used in tarantism.metaclasses.ModelMetaclass to sort fields.
    creation_counter = 0

    # Used for field_types in tarantool client filter method.
    tarantool_filter_type = str

    def __init__(self,
                 required=True,
                 default=None,
                 primary_key=False,
                 db_index=None,
                 verbose_name=None,
                 help_text=None):
        self.required = required
        self.default = default
        self.primary_key = primary_key
        self.db_index = db_index
        self.verbose_name = verbose_name
        self.help_text = help_text

        self.creation_counter = BaseField.creation_counter
        BaseField.creation_counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return instance._data.get(self.name)

    def __set__(self, instance, value):
        if value is None and self.default is not None:
            value = self.default
            if callable(value):
                value = value()

        instance._data[self.name] = value

    def to_python(self, value):
        return value

    def to_db(self, value):
        return self.to_python(value)

    def validate(self, value):
        pass


class Num32Field(BaseField):
    MIN = INT32_MIN
    MAX = INT32_MAX

    # Used for field_types in tarantool client filter method.
    tarantool_filter_type = int

    type_factory = int

    def __init__(self, min_value=None, max_value=None, **kwargs):
        min_value = min_value or self.MIN
        max_value = max_value or self.MAX

        if min_value < self.MIN:
            raise ValueError('min_value can not be less than {}.'.format(self.MIN))

        if max_value > self.MAX:
            raise ValueError('max_value can not be greater than {}.'.format(self.MAX))

        self.min_value = min_value
        self.max_value = max_value

        super(Num32Field, self).__init__(**kwargs)

    def to_python(self, value):
        return self.type_factory(value)

    def validate(self, value):
        try:
            value = self.type_factory(value)
        except ValueError:
            raise ValidationError(
                '{name} field error: '
                'Invalid {value} for field {field_class}.'.format(
                    name=self.name, value=value, field_class=self.__class__.__name__
                )
            )

        if self.min_value is not None and value < self.min_value:
            raise ValidationError(
                '{name} field error: '
                'value {value} is less than {min_value}'.format(
                    name=self.name, value=value, min_value=self.min_value
                )
            )

        if self.max_value is not None and value > self.max_value:
            raise ValidationError(
                '{name} field error: '
                'value {value} is greater than {max_value}'.format(
                    name=self.name, value=value, max_value=self.max_value
                )
            )


class Num64Field(Num32Field):
    MIN = INT64_MIN
    MAX = INT64_MAX

    tarantool_filter_type = long

    type_factory = long


class BytesField(BaseField):
    def __init__(self,
                 regex=None,
                 max_length=None,
                 min_length=None,
                 **kwargs):
        self.regex = re.compile(regex) if regex else None
        self.max_length = max_length
        self.min_length = min_length

        super(BytesField, self).__init__(**kwargs)

    def validate(self, value):
        if not isinstance(value, basestring):
            raise ValidationError(
                '{name} field error: '
                'Invalid {value} for field {field_class}.'.format(
                    name=self.name, value=value, field_class=self.__class__.__name__
                )
            )

        if self.min_length is not None and len(value) < self.min_length:
            raise ValidationError(
                '{name} field error: '
                'value {value} length is less than {min_length}'.format(
                    name=self.name, value=value, min_length=self.min_length
                )
            )

        if self.max_length is not None and len(value) > self.max_length:
            raise ValidationError(
                '{name} field error: '
                'value {value} length is greater than {max_length}'.format(
                    name=self.name, value=value, max_length=self.max_length
                )
            )

        if self.regex is not None and self.regex.match(value) is None:
            raise ValidationError(
                '{name} field error: '
                'value {value} did not match validation regex.'.format(
                    name=self.name, value=value
                )
            )


class StringField(BytesField):
    tarantool_filter_type = unicode

    def to_db(self, value):
        return value.encode('utf8')

    def to_python(self, value):
        return value.decode('utf8')


DEFAULT_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'


class DateTimeField(BaseField):
    def __init__(self,
                 datetime_format=DEFAULT_DATETIME_FORMAT,
                 **kwargs):
        self.datetime_format = datetime_format

        super(DateTimeField, self).__init__(**kwargs)

    def to_db(self, value):
        return value.strftime(self.datetime_format)

    def to_python(self, value):
        return datetime.strptime(value, self.datetime_format)

    def validate(self, value):
        if not isinstance(value, datetime):
            raise ValidationError(
                '{name} field error: '
                '{value} has incorrect type {type}.'.format(
                    name=self.name, value=value, type=type(value)
                )
            )


class DecimalField(BaseField):
    def __init__(self, **kwargs):
        super(DecimalField, self).__init__(**kwargs)

    def to_db(self, value):
        return str(value)

    def to_python(self, value):
        return Decimal(value)
