
from tarantism import Model
from tarantism import LongField
from tarantism import StringField
from tarantism.tests import TestCase


class ModelDefaultsTestCase(TestCase):
    def test_defaults(self):
        default_pk = 1L
        default_data = u'Test data'

        class Record(Model):
            pk = LongField(default=default_pk)
            data = StringField(default=default_data)

        r = Record()

        self.assertEqual(default_pk, r.pk)
        self.assertEqual(default_data, r.data)


class ModelInitTestCase(TestCase):
    def test_init(self):
        pk = 1L
        data = u'test'

        class Record(Model):
            pk = LongField()
            data = StringField()

        r = Record(pk=pk, data=data)

        self.assertEqual(pk, r.pk)
        self.assertEqual(data, r.data)


class ModelSettersTestCase(TestCase):
    def test_setters(self):
        pk = 1L
        data = u'test'

        class Record(Model):
            pk = LongField()
            data = StringField()

        r = Record()
        r.pk = pk
        r.data = data

        self.assertEqual(pk, r.pk)
        self.assertEqual(data, r.data)


class ModelDictLikeTestCase(TestCase):
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

    def test_get_defined_fields(self):
        data = {
            'pk': 1L,
            'data': u'test'
        }

        class Record(Model):
            pk = LongField()
            data = StringField()

        r = Record(**data)

        for key, value in data.iteritems():
            self.assertEqual(value, r[key])

    def test_get_not_defined_field(self):
        class Record(Model):
            pk = LongField()
            data = StringField()

        r = Record()
        with self.assertRaises(KeyError):
            r['not_defined_field']

    def test_set_defined_fields(self):
        pk = 1L
        data = u'test'

        class Record(Model):
            pk = LongField()
            data = StringField()

        r = Record()
        r['pk'] = pk
        r['data'] = data

        self.assertEqual(pk, r.pk)
        self.assertEqual(data, r.data)

    def test_set_not_defined_field(self):
        class Record(Model):
            pk = LongField()
            data = StringField()

        r = Record()

        with self.assertRaises(KeyError):
            r['not_defined_field'] = 1L
