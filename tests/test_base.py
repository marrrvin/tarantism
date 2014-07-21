
import unittest

from tarantism import DEFAULT_ALIAS
from tarantism import register_connection
from tarantism import get_space
from tarantism import Model
from tarantism import Num64Field
from tarantism import StrField


class Record(Model):
    pk = Num64Field()
    data = StrField()


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.tnt_config = {
            'host': '127.0.0.1',
            'port': 33013,
            'space': 0
        }

        register_connection(DEFAULT_ALIAS, **self.tnt_config)
        space = get_space()
        space.connection.call(
            'clear_space', (str(self.tnt_config['space']),)
        )

    def test_create(self):
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

        self.assertRaises(Record.DoesNotExist, Record.objects.get, pk)
