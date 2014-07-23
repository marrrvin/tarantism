
from unittest import TestCase

from tarantism import Model
from tarantism import LongField
from tarantism import StringField
from tarantism.errors import ValidationError


class ValidationTestCase(TestCase):
    def test_fail_required(self):
        class Record(Model):
            pk = LongField(required=True)
            data = StringField(default='')

        r = Record()

        self.assertRaises(ValidationError, r.validate)

    def test_pass_validation(self):
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

    def test_fail_validation(self):
        class Record(Model):
            pk = LongField(
                min_value=0
            )
            data = StringField(
                min_length=1,
                max_length=1
            )

        r = Record(pk=-1L, data='test')

        self.assertRaises(ValidationError, r.validate)
