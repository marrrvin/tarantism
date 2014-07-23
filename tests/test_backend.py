
from unittest import TestCase

from tarantism import DEFAULT_ALIAS
from tarantism import register_connection
from tarantism import get_space
from tarantism import Model
from tarantism import LongField
from tarantism import StringField


class DatabaseTestCase(TestCase):
    def setUp(self):
        self.tnt_config = {
            'host': '127.0.0.1',
            'port': 33013,
            'space': 0
        }

        register_connection(DEFAULT_ALIAS, **self.tnt_config)

        self.space = get_space()
        self.space.connection.call(
            'clear_space', (str(self.tnt_config['space']),)
        )


class SaveModelTestCase(DatabaseTestCase):
    def test_save(self):
        class Record(Model):
            pk = LongField(
                required=True
            )
            data = StringField()

        pk = 1L

        r = Record(pk=pk, data='test')
        r.save()

        response = self.space.select(pk)

        actual_record = response[0]
        self.assertEqual(r.pk, int(actual_record[0]))
        self.assertEqual(r.data, actual_record[1])



class LoadModelTestCase(DatabaseTestCase):
    def test_load_existent(self):
        """
        """

    def test_load_non_existent(self):
        """
        """


class DeleteModelTestCase(DatabaseTestCase):
    def test_delete_existent(self):
        """
        record.delete()
        """

    def test_delete_non_existent(self):
        """
        self.assertRaises(Record.DoesNotExist, Record.objects.get, pk)
        """
