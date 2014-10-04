
from unittest2 import TestCase

from tarantism import Model
from tarantism import LongField
from tarantism import StringField


class ModelTestCase(TestCase):
    def test_defaults(self):
        default_pk = 1L
        default_data = u'Test data'

        class Record(Model):
            pk = LongField(default=default_pk)
            data = StringField(default=default_data)

        r = Record()

        self.assertEqual(default_pk, r.pk)
        self.assertEqual(default_data, r.data)

    def test_create(self):
        class Record(Model):
            pk = LongField()
            data = StringField()

        pk = 1L
        data = 'test'

        r = Record(pk=pk, data=data)

        self.assertEqual(pk, r.pk)
        self.assertEqual(data, r.data)

    def test_setters(self):
        class Record(Model):
            pk = LongField()
            data = StringField()

        pk = 1L
        data = 'test'

        r = Record()
        r.pk = pk
        r.data = data

        self.assertEqual(pk, r.pk)
        self.assertEqual(data, r.data)
