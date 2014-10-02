
from unittest2 import TestCase

from tarantism import Model
from tarantism import BaseField
from tarantism import IntField
from tarantism import LongField
from tarantism import StringField
from tarantism import ValidationError


class BaseFieldTestCase(TestCase):
    def test_simple(self):
        field = BaseField()
        value = u'test'

        self.assertEqual(value, field.to_python(value))


class FieldRequiredValidationTestCase(TestCase):
    def test_fail_on_required_field(self):
        class Record(Model):
            pk = LongField()

        r = Record()

        self.assertRaises(ValidationError, r.validate)


class IntFieldValidationTestCase(TestCase):
    def test_fail_on_invalid_type(self):
        class Record(Model):
            pk = IntField(min_value=1)

        r = Record(pk='invalid-pk')
        self.assertRaises(ValidationError, r.validate)

    def test_fail_on_min_value(self):
        class Record(Model):
            pk = IntField(min_value=1)

        r = Record(pk=-1L)

        self.assertRaises(ValidationError, r.validate)

    def test_fail_on_max_value(self):
        class Record(Model):
            pk = IntField(max_value=1)

        r = Record(pk=2L)

        self.assertRaises(ValidationError, r.validate)


class LongFieldValidationTestCase(TestCase):
    def test_fail_on_invalid_type(self):
        class Record(Model):
            pk = LongField(min_value=1)

        r = Record(pk='invalid-pk')
        self.assertRaises(ValidationError, r.validate)

    def test_fail_on_min_value(self):
        class Record(Model):
            pk = LongField(min_value=1)

        r = Record(pk=-1L)

        self.assertRaises(ValidationError, r.validate)

    def test_fail_on_max_value(self):
        class Record(Model):
            pk = LongField(max_value=1)

        r = Record(pk=2L)

        self.assertRaises(ValidationError, r.validate)


class StringFieldValidationTestCase(TestCase):
    def test_fail_on_min_length(self):
        class Record(Model):
            data = StringField(min_length=1)

        r = Record(data=u'')

        self.assertRaises(ValidationError, r.validate)

    def test_fail_on_max_length(self):
        class Record(Model):
            data = StringField(max_length=1)

        r = Record(data=u'test')

        self.assertRaises(ValidationError, r.validate)

    def test_fail_on_regex(self):
        class Record(Model):
            data = StringField(regex=u'^\d+$')

        r = Record(data=u'123test45')

        self.assertRaises(ValidationError, r.validate)


class ValidationPassedTestCase(TestCase):
    def test_pass(self):
        class Record(Model):
            pk = LongField(min_value=0)
            data = StringField(min_length=1, max_length=100)

        r = Record(pk=1L, data='test')

        self.assertEqual(None, r.validate())
