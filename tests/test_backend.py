
from unittest2 import TestCase

import tarantism.connection
from tarantism import DEFAULT_ALIAS
from tarantism import register_connection
from tarantism import get_space
from tarantism import disconnect
from tarantism import Model
from tarantism import LongField
from tarantism import StringField
from tarantism import DoesNotExist


class DatabaseTestCase(TestCase):
    def setUp(self):
        self.tnt_config = {
            'host': '127.0.0.1',
            'port': 33013,
            'space': 0
        }
        register_connection(DEFAULT_ALIAS, **self.tnt_config)

        self.space = get_space()

    def tearDown(self):
        self.space.connection.call(
            'clear_space', (str(self.tnt_config['space']),)
        )

        disconnect()

        setattr(tarantism.connection, '_connection_settings', {})
        setattr(tarantism.connection, '_connections', {})
        setattr(tarantism.connection, '_spaces', {})


class SaveModelTestCase(DatabaseTestCase):
    def test_save(self):
        class Record(Model):
            pk = LongField()
            data = StringField()

        pk = 1L

        r = Record(pk=pk, data='test')
        r.save()

        response = self.space.select(pk)

        actual_record = response[0]
        self.assertEqual(r.pk, int(actual_record[0]))
        self.assertEqual(r.data, actual_record[1])


class DeleteModelTestCase(DatabaseTestCase):
    def test_delete_existent(self):
        class Record(Model):
            pk = LongField()
            data = StringField()

        pk = 1L

        r = Record(pk=pk, data=u'test')
        r.save()
        r.delete()

        with self.assertRaises(DoesNotExist):
            Record.objects.get(pk=pk)

    def test_delete_non_default_primary_key(self):
        class Record(Model):
            id = LongField(
                primary_key=True,
                db_index=0
            )
            data = StringField()

        user_id = 1L
        data = u'test'

        r = Record(id=user_id, data=data)
        r.save()
        r.delete()

        with self.assertRaises(DoesNotExist):
            Record.objects.get(id=user_id)

    def test_delete_primary_key_not_defined(self):
        class Record(Model):
            id = LongField(
                db_index=0
            )
            data = StringField()

        user_id = 1L
        data = u'test'

        r = Record(id=user_id, data=data)
        r.save()

        with self.assertRaises(ValueError):
            r.delete()


class ManagerGetTestCase(DatabaseTestCase):
    def test_get_does_not_exist(self):
        class Record(Model):
            pk = LongField()
            data = StringField()

        with self.assertRaises(Record.DoesNotExist):
            Record.objects.get(pk=1L)

    def test_get_non_existent_field(self):
        class Record(Model):
            pk = LongField()
            data = StringField()

        with self.assertRaises(ValueError):
            Record.objects.get(non_existent_field=1L)

    def test_get_primary_key_not_defined(self):
        class Record(Model):
            data = StringField()

        with self.assertRaises(ValueError):
            Record.objects.get(data=u'test')

    def test_get_non_default_index(self):
        class Record(Model):
            user_id = LongField(db_index=0)
            data = StringField()

        user_id = 1L
        data = u'test'

        r1 = Record(user_id=user_id, data=data)
        r1.save()

        r2 = Record.objects.get(user_id=user_id)

        self.assertEqual(data, r2.data)
