# coding: utf8

from datetime import datetime
from decimal import Decimal

from tarantism import Model
from tarantism import BaseField
from tarantism import StringField
from tarantism import BytesField
from tarantism import DateTimeField
from tarantism import DecimalField
from tarantism import ValidationError
from tarantism import Num32Field
from tarantism import Num64Field
from tarantism import INT32_MIN
from tarantism import INT32_MAX
from tarantism import INT64_MIN
from tarantism import INT64_MAX
from tarantism.tests import TestCase


class BaseFieldTestCase(TestCase):
    def test_public_interface(self):
        field = BaseField()
        value = u'test'

        self.assertEqual(value, field.to_python(value))
        self.assertIsNone(field.validate(value))
        self.assertEqual(str, field._get_tarantool_type())

    def test_descriptor(self):
        field = BaseField()
        instance = None
        owner = object()

        self.assertEqual(
            BaseField.__get__(field, instance, owner), field
        )


class FieldRequiredValidationTestCase(TestCase):
    def test_fail_on_required_field(self):
        class Record(Model):
            pk = Num64Field(required=True)

        r = Record()

        with self.assertRaises(ValidationError):
            r.validate()

    def test_fail_on_required_field_by_default(self):
        class Record(Model):
            pk = Num64Field()

        r = Record()

        with self.assertRaises(ValidationError):
            r.validate()


class Num32FieldValidationTestCase(TestCase):
    def test_fail_on_invalid_type(self):
        value = 'invalid-value'
        field = Num32Field(min_value=1)

        with self.assertRaises(ValidationError):
            field.validate(value)

    def test_fail_on_default_min_value(self):
        value = INT32_MIN - 1
        field = Num32Field()

        with self.assertRaises(ValidationError):
            field.validate(value)

    def test_fail_on_default_max_value(self):
        value = INT32_MAX + 1
        field = Num32Field()

        with self.assertRaises(ValidationError):
            field.validate(value)

    def test_fail_on_min_value(self):
        value = -1
        field = Num32Field(min_value=1)

        with self.assertRaises(ValidationError):
            field.validate(value)

    def test_fail_on_max_value(self):
        value = 2L
        field = Num32Field(max_value=1)

        with self.assertRaises(ValidationError):
            field.validate(value)

    def test_invalid_min_value(self):
        with self.assertRaises(ValueError):
            Num32Field(min_value=INT32_MIN - 1)

    def test_invalid_max_value(self):
        with self.assertRaises(ValueError):
            Num32Field(max_value=INT32_MAX + 1)


class Num64FieldValidationTestCase(TestCase):
    def test_fail_on_invalid_type(self):
        value = 'invalid-value'
        field = Num64Field(min_value=1)

        with self.assertRaises(ValidationError):
            field.validate(value)

    def test_fail_on_default_min_value(self):
        value = INT64_MIN - 1
        field = Num32Field()

        with self.assertRaises(ValidationError):
            field.validate(value)

    def test_fail_on_default_max_value(self):
        value = INT64_MAX + 1
        field = Num32Field()

        with self.assertRaises(ValidationError):
            field.validate(value)

    def test_fail_on_min_value(self):
        value = -1L
        field = Num64Field(min_value=1)

        with self.assertRaises(ValidationError):
            field.validate(value)

    def test_fail_on_max_value(self):
        value = 2L
        field = Num64Field(max_value=1)

        with self.assertRaises(ValidationError):
            field.validate(value)

    def test_invalid_min_value(self):
        with self.assertRaises(ValueError):
            Num64Field(min_value=INT64_MIN - 1)

    def test_invalid_max_value(self):
        with self.assertRaises(ValueError):
            Num64Field(max_value=INT64_MAX + 1)


class StringFieldSerializationTestCase(TestCase):
    def test_non_ascii_chars(self):
        value = u'тест'
        field = StringField()

        value_to_db = field.to_db(value)
        value_to_python = field.to_python(value_to_db)

        self.assertIsInstance(value_to_db, str)
        self.assertIsInstance(value_to_python, unicode)
        self.assertEqual(value_to_python, value)


class StringFieldValidationTestCase(TestCase):
    def test_fail_on_invalid_type(self):
        value = {}
        field = StringField()

        with self.assertRaises(ValidationError):
            field.validate(value)

    def test_fail_on_min_length(self):
        value = u''
        field = StringField(min_length=1)

        with self.assertRaises(ValidationError):
            field.validate(value)

    def test_fail_on_max_length(self):
        value = u'test'
        field = StringField(max_length=1)

        with self.assertRaises(ValidationError):
            field.validate(value)

    def test_fail_on_regex(self):
        value = u'123test45'
        field = StringField(regex=u'^\d+$')

        with self.assertRaises(ValidationError):
            field.validate(value)


class BytesFieldValidationTestCase(TestCase):
    def test_fail_on_invalid_type(self):
        value = {}
        field = BytesField()

        with self.assertRaises(ValidationError):
            field.validate(value)

    def test_fail_on_min_length(self):
        value = u''
        field = BytesField(min_length=1)

        with self.assertRaises(ValidationError):
            field.validate(value)

    def test_fail_on_max_length(self):
        value = u'test'
        field = BytesField(max_length=1)

        with self.assertRaises(ValidationError):
            field.validate(value)

    def test_fail_on_regex(self):
        value = u'123test45'
        field = BytesField(regex=u'^\d+$')

        with self.assertRaises(ValidationError):
            field.validate(value)


class DateTimeFieldValidationTestCase(TestCase):
    def test_fail_on_invalid_type(self):
        value = {}
        field = DateTimeField()

        with self.assertRaises(ValidationError):
            field.validate(value)


class DateTimeFieldSerializationTestCase(TestCase):
    def test_base(self):
        value = datetime.now()
        field = DateTimeField()

        value_to_db = field.to_db(value)
        value_to_python = field.to_python(value_to_db)

        self.assertIsInstance(value_to_db, str)
        self.assertIsInstance(value_to_python, datetime)
        self.assertEqual(value_to_python, value)


class DecimalFieldSerializationTestCase(TestCase):
    def test_base(self):
        value = Decimal('1.01')
        field = DecimalField()

        value_to_db = field.to_db(value)
        value_to_python = field.to_python(value_to_db)

        self.assertIsInstance(value_to_db, str)
        self.assertIsInstance(value_to_python, Decimal)
        self.assertEqual(value_to_python, value)


class ValidationOkTestCase(TestCase):
    def test_ok(self):
        class Record(Model):
            pk = Num64Field(min_value=0)
            data = StringField(min_length=1, max_length=100)

        r = Record(pk=1L, data=u'test')

        self.assertIsNone(r.validate())
