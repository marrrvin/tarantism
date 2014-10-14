# coding: utf8

from tarantism import Model
from tarantism import BaseField
from tarantism import IntField
from tarantism import LongField
from tarantism import StringField
from tarantism import BytesField
from tarantism import ValidationError
from tarantism.tests import TestCase


class BaseFieldTestCase(TestCase):
    def test_interface_behaviour(self):
        value = u'test'
        field = BaseField()

        self.assertEqual(value, field.to_python(value))
        self.assertIsNone(field.validate(value))

        with self.assertRaises(NotImplementedError):
            field.python_type

        with self.assertRaises(NotImplementedError):
            field.db_type


class FieldRequiredValidationTestCase(TestCase):
    def test_fail_on_required_field(self):
        class Record(Model):
            pk = LongField(required=True)

        r = Record()

        with self.assertRaises(ValidationError):
            r.validate()

    def test_fail_on_required_field_by_default(self):
        class Record(Model):
            pk = LongField()

        r = Record()

        with self.assertRaises(ValidationError):
            r.validate()


class IntFieldValidationTestCase(TestCase):
    def test_fail_on_invalid_type(self):
        value = 'invalid-value'
        field = IntField(min_value=1)

        with self.assertRaises(ValidationError):
            field.validate(value)

    def test_fail_on_min_value(self):
        value = -1
        field = IntField(min_value=1)

        with self.assertRaises(ValidationError):
            field.validate(value)

    def test_fail_on_max_value(self):
        value = 2L
        field = IntField(max_value=1)

        with self.assertRaises(ValidationError):
            field.validate(value)


class LongFieldValidationTestCase(TestCase):
    def test_fail_on_invalid_type(self):
        value = 'invalid-value'
        field = LongField(min_value=1)

        with self.assertRaises(ValidationError):
            field.validate(value)

    def test_fail_on_min_value(self):
        value = -1L
        field = LongField(min_value=1)

        with self.assertRaises(ValidationError):
            field.validate(value)

    def test_fail_on_max_value(self):
        value = 2L
        field = LongField(max_value=1)

        with self.assertRaises(ValidationError):
            field.validate(value)


class StringFieldSerializationTestCase(TestCase):
    def test_non_ascii_chars(self):
        value = u'тест'
        field = StringField()

        value_to_db = field.to_db(value)
        value_to_python = field.to_python(value_to_db)

        self.assertIsInstance(value_to_db, str)
        self.assertIsInstance(value_to_python, unicode)


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


class ValidationOkTestCase(TestCase):
    def test_ok(self):
        class Record(Model):
            pk = LongField(min_value=0)
            data = StringField(min_length=1, max_length=100)

        r = Record(pk=1L, data='test')

        self.assertIsNone(r.validate())
