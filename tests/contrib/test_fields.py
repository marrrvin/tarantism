
import json

from tarantism.tests import TestCase
from tarantism.contrib.fields import JsonField
from tarantism.contrib.fields import ProtobufField


class JsonFieldSerializationTestCase(TestCase):
    def test_ok(self):
        value = {
            'key1': u'value1',
            'key2': 8,
            'key3': [0, 1, 2]
        }
        field = JsonField()

        value_to_db = field.to_db(value)
        value_to_python = field.to_python(value_to_db)

        self.assertEqual(value_to_db, json.dumps(value))
        self.assertEqual(value_to_python, value)


class ProtobufFieldSerializationTestCase(TestCase):
    def test_ok(self):
        from .message_pb2 import User

        field = ProtobufField(User)

        user = User()
        user.id = 1
        user.name = 'name'
        user.email = 'test@example.com'

        value_to_db = field.to_db(user)
        value_to_python = field.to_python(value_to_db)

        self.assertEqual(value_to_db, user.SerializeToString())
        self.assertEqual(value_to_python, user)
