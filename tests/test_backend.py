
from tarantism import DEFAULT_ALIAS
from tarantism import register_connection
from tarantism import get_space
from tarantism import disconnect
from tarantism import models
from tarantism import DoesNotExist
from tarantism.tests import TestCase


class DatabaseTestCase(TestCase):
    def setUp(self):
        self.tnt_config = {
            'host': '127.0.0.1',
            'port': 33013,
        }
        self.another_space_alias = 'the_new_space'

        register_connection(
            DEFAULT_ALIAS, space=0, **self.tnt_config
        )
        register_connection(
            self.another_space_alias, space=1, **self.tnt_config
        )

        self.space = get_space(DEFAULT_ALIAS)
        self.another_space = get_space(self.another_space_alias)

    def tearDown(self):
        self.space.connection.call('clear_space', ('0',))
        self.another_space.connection.call('clear_space', ('1',))

        disconnect(DEFAULT_ALIAS)
        disconnect(self.another_space_alias)


class ModelSaveTestCase(DatabaseTestCase):
    def test_save(self):
        class Record(models.Model):
            pk = models.LongField()
            data = models.StringField()

        pk = 1L

        r = Record(pk=pk, data='test')
        returned_value = r.save()

        self.assertIsInstance(returned_value, Record)

        response = self.space.select(pk)

        actual_record = response[0]
        self.assertEqual(r.pk, int(actual_record[0]))
        self.assertEqual(r.data, actual_record[1])


class ModelDeleteTestCase(DatabaseTestCase):
    def test_delete_existent(self):
        pk = 1L

        class Record(models.Model):
            pk = models.LongField()
            data = models.StringField()
            secondary_key = models.IntField()

        r = Record(pk=pk, data=u'test', secondary_key=1L)
        r.save()
        returned_value = r.delete()

        self.assertIsInstance(returned_value, Record)

        with self.assertRaises(DoesNotExist):
            Record.objects.get(pk=pk)

    def test_delete_non_default_primary_key(self):
        user_id = 1L
        data = u'test'

        class Record(models.Model):
            id = models.LongField(
                primary_key=True,
                db_index=0
            )
            data = models.StringField()

        r = Record(id=user_id, data=data)
        r.save()
        r.delete()

        with self.assertRaises(DoesNotExist):
            Record.objects.get(id=user_id)

    def test_delete_primary_key_not_defined(self):
        user_id = 1L
        data = u'test'

        class Record(models.Model):
            id = models.LongField(
                db_index=0
            )
            data = models.StringField()

        r = Record(id=user_id, data=data)
        r.save()

        with self.assertRaises(ValueError):
            r.delete()


class ModelUpdateTestCase(DatabaseTestCase):
    def test_update(self):
        pk = 1L
        init_value = u'test1'
        new_value = u'test2'

        class Record(models.Model):
            pk = models.LongField()
            data = models.StringField()

        r = Record(pk=pk, data=init_value)
        r.save()

        return_value = r.update(data=new_value)

        self.assertIsInstance(return_value, Record)
        self.assertEqual(return_value.data, new_value)

        r2 = Record.objects.get(pk=pk)
        self.assertEqual(new_value, r2.data)

    def test_update_unknown_operation(self):
        class Record(models.Model):
            pk = models.LongField()
            counter = models.IntField()

        r = Record(pk=1L, counter=1)
        r.save()

        with self.assertRaises(ValueError):
            r.update(counter__unknown=10)

    def test_update_add(self):
        class Record(models.Model):
            pk = models.LongField()
            counter = models.IntField()

        r = Record(pk=1L, counter=1)
        r.save()

        r.update(counter__add=10)

        r2 = Record.objects.get(pk=1L)
        self.assertEqual(11, r2.counter)


class ManagerGetTestCase(DatabaseTestCase):
    def test_get_does_not_exist(self):
        class Record(models.Model):
            pk = models.LongField()
            data = models.StringField()

        with self.assertRaises(Record.DoesNotExist):
            Record.objects.get(pk=1L)

    def test_get_multiple_objects_returned(self):
        class Record(models.Model):
            id = models.LongField()
            user_id = models.LongField(db_index=1)
            data = models.StringField()

            meta = {
                'db_alias': self.another_space_alias
            }

        r1 = Record(id=1L, user_id=1L, data=u'test1')
        r1.save()
        r2 = Record(id=2L, user_id=1L, data=u'test2')
        r2.save()

        with self.assertRaises(Record.MultipleObjectsReturned):
            Record.objects.get(user_id=1L)

    def test_get_non_existent_field(self):
        class Record(models.Model):
            pk = models.LongField()
            data = models.StringField()

        with self.assertRaises(ValueError):
            Record.objects.get(non_existent_field=1L)

    def test_get_primary_key_not_defined(self):
        class Record(models.Model):
            data = models.StringField()

        with self.assertRaises(ValueError):
            Record.objects.get(data=u'test')

    def test_get_non_default_index(self):
        user_id = 1L
        data = u'test'

        class Record(models.Model):
            user_id = models.LongField(db_index=0)
            data = models.StringField()

        r1 = Record(user_id=user_id, data=data)
        r1.save()

        r2 = Record.objects.get(user_id=user_id)

        self.assertEqual(data, r2.data)


class ManagerFilterTestCase(DatabaseTestCase):
    def test_get_empty_list(self):
        class Record(models.Model):
            pk = models.LongField()
            data = models.StringField()

        records = Record.objects.filter(pk=1L)

        self.assertIsInstance(records, list)
        self.assertEqual(0, len(records))

    def test_get_list(self):
        user_id = 1L
        data = u'test1'

        class Record(models.Model):
            pk = models.LongField()
            user_id = models.LongField(db_index=1)
            data = models.StringField()

            meta = {
                'db_alias': self.another_space_alias
            }

        r1 = Record(pk=1L, user_id=user_id, data=data)
        r1.save()
        r2 = Record(pk=2L, user_id=user_id, data=data)
        r2.save()

        records = Record.objects.filter(user_id=user_id)

        self.assertIsInstance(records, list)
        self.assertEqual(2, len(records))

        for r in records:
            self.assertIsInstance(r, models.Model)
            self.assertEqual(user_id, r.user_id)
            self.assertIsInstance(r.user_id, long)
            self.assertEqual(data, r.data)
            self.assertIsInstance(data, unicode)


class ManagerCreateTestCase(DatabaseTestCase):
    def test_create(self):
        pk = 1L
        data = u'test'

        class Record(models.Model):
            pk = models.LongField()
            data = models.StringField()

        r = Record.objects.create(pk=pk, data=data)

        self.assertIsInstance(r, models.Model)
        self.assertEqual(data, r.data)
        self.assertEqual(pk, r.pk)
