
from unittest import TestCase

from tarantism import Model
from tarantism import LongField
from tarantism import StringField
from tarantism import ValidationError


class ValidationTestCase(TestCase):
    def test_fail_on_required_field(self):
        class Record(Model):
            pk = LongField()
            data = StringField()

        r = Record()

        self.assertRaises(ValidationError, r.validate)

    def test_fail_on_field_too_long(self):
        class Record(Model):
            pk = LongField()
            data = StringField(
                min_length=1, max_length=1
            )

        r = Record(pk=1L, data='test')

        self.assertRaises(ValidationError, r.validate)

    def test_fail_on_field_value_too_small(self):
        class Record(Model):
            pk = LongField(min_value=1)
            data = StringField()

        r = Record(pk=-1L, data='test')

        self.assertRaises(ValidationError, r.validate)

    def test_pass(self):
        class Record(Model):
            pk = LongField(
                min_value=0
            )
            data = StringField(
                min_length=1,
                max_length=100
            )

        r = Record(pk=1L, data='test')

        self.assertEqual(None, r.validate())


class DefaultsTestCase(TestCase):
    def test_defaults(self):
        default_pk = 1L
        default_data = u'Test data'

        class Record(Model):
            pk = LongField(default=default_pk)
            data = StringField(default=default_data)

        r = Record()

        self.assertEqual(default_pk, r.pk)
        self.assertEqual(default_data, r.data)
