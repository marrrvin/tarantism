
from unittest import TestCase

from tarantism import Model
from tarantism import LongField
from tarantism import StringField


class CreateModelTestCase(TestCase):
    def test_default(self):
        class Record(Model):
            pk = LongField()
            data = StringField(default='test')

        r = Record()

        self.assertEqual('test', r.data)

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
