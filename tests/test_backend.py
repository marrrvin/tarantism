
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
        space = get_space()
        space.connection.call(
            'clear_space', (str(self.tnt_config['space']),)
        )


class SaveModelTestCase(DatabaseTestCase):
    def test_save(self):
        """
        class Record(Model):
            pk = LongField()
            data = StringField()

        r = Record()

        actual_r = r.save()

        self.assertEqual(r.pk, actual_r.pk)
        self.assertEqual(r.data, actual_r.data)
        """


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
