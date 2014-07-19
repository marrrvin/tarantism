
import unittest

from tarantism import initialize
from tarantism import Model
from tarantism import Num64Field
from tarantism import StrField


class Record(Model):
    pk = Num64Field()
    data = StrField()


class BaseTestCase(unittest.TestCase):
    def test_create(self):
        initialize(host='127.0.0.1', port=33013, space=0)
        pk = 1L
        Record.objects.delete(pk)
        record = Record(
            pk=pk,
            data='test'
        )
        record.save()

        actual_record = Record.objects.get(pk)

        self.assertEqual(record.pk, actual_record.pk)
        self.assertEqual(record.data, actual_record.data)

        record.delete()

        with self.assertRaises(Record.DoesNotExist):
            Record.objects.get(pk)
