
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

    def test_iter(self):
        class Record(Model):
            pk = LongField()
            data = StringField()

        data = {
            'pk': 1L,
            'data': u'test'
        }

        r = Record(**data)

        for i, field_name in enumerate(r):
            self.assertEqual(data[field_name], getattr(r, field_name))

    def test_dict_get_fields_ok(self):
        class Record(Model):
            pk = LongField()
            data = StringField()

        data = {
            'pk': 1L,
            'data': u'test'
        }

        r = Record(**data)

        for key, value in data.iteritems():
            self.assertEqual(value, r[key])

    def test_dict_get_not_defined_field(self):
        class Record(Model):
            pk = LongField()
            data = StringField()

        r = Record()
        with self.assertRaises(KeyError):
            r['not_defined_field']

    def test_dict_set_field(self):
        class Record(Model):
            pk = LongField()
            data = StringField()

        pk = 1L
        r = Record()
        r['pk'] = pk

        self.assertEqual(pk, r.pk)

    def test_dict_set_not_defined_field(self):
        class Record(Model):
            pk = LongField()
            data = StringField()

        r = Record()

        with self.assertRaises(KeyError):
            r['not_defined_field'] = 1L
