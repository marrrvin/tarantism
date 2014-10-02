
from unittest2 import TestCase
from mock import patch

from tarantool import Connection
from tarantool.space import Space

from tarantism import register_connection
from tarantism import connect
from tarantism import disconnect
from tarantism import get_connection
from tarantism import get_space
from tarantism import ConnectionError


class ConnectionTestCase(TestCase):
    def assert_connection(self, connection, host, port):
        self.assertIsInstance(connection, Connection)
        self.assertEqual(True, connection.connected)
        self.assertEqual(host, connection.host)
        self.assertEqual(port, connection.port)

    def assert_space(self, space, space_no):
        self.assertIsInstance(space, Space)
        self.assertEqual(space.space_no, space_no)

    def setUp(self):
        self.alias = 'test'
        self.host = '127.0.0.1'
        self.port = 33013
        self.space = 0

    @patch.dict('tarantism.connection._connection_settings', {'q': {}})
    @patch.dict('tarantism.connection._connections', {'q': {}})
    @patch.dict('tarantism.connection._spaces', {'q': {}})
    def test_register_connection(self):
        expected_connection_settings = {
            'host': self.host,
            'port': self.port,
            'space': self.space
        }

        connection_settings = register_connection(
            self.alias, host=self.host, port=self.port
        )
        self.assertEqual(connection_settings, expected_connection_settings)

    @patch.dict('tarantism.connection._connection_settings', {'q': {}})
    @patch.dict('tarantism.connection._connections', {'q': {}})
    @patch.dict('tarantism.connection._spaces', {'q': {}})
    def test_get_connection_non_existent_alias(self):
        non_existent_alias = 'unknown'
        self.assertRaises(ValueError, get_connection, non_existent_alias)

    @patch.dict('tarantism.connection._connection_settings', {'q': {}})
    @patch.dict('tarantism.connection._connections', {'q': {}})
    @patch.dict('tarantism.connection._spaces', {'q': {}})
    def test_get_connection_with_reconnect(self):
        connect(
            self.alias, host=self.host, port=self.port, space=self.space
        )
        connection = get_connection(self.alias, reconnect=True)
        self.assert_connection(connection, self.host, self.port)

    @patch.dict('tarantism.connection._connection_settings', {'q': {}})
    @patch.dict('tarantism.connection._connections', {'q': {}})
    @patch.dict('tarantism.connection._spaces', {'q': {}})
    def test_connect_ok(self):
        connection = connect(
            self.alias, host=self.host, port=self.port, space=self.space
        )
        self.assert_connection(connection, self.host, self.port)

    @patch.dict('tarantism.connection._connection_settings', {'q': {}})
    @patch.dict('tarantism.connection._connections', {'q': {}})
    @patch.dict('tarantism.connection._spaces', {'q': {}})
    def test_connect_error(self):
        invalid_host = '127.0.0.2'
        invalid_port = 34013

        self.assertRaises(
            ConnectionError,
            connect,
            self.alias, host=invalid_host, port=invalid_port, space=self.space
        )

    @patch.dict('tarantism.connection._connection_settings', {'q': {}})
    @patch.dict('tarantism.connection._connections', {'q': {}})
    @patch.dict('tarantism.connection._spaces', {'q': {}})
    def test_disconnect_non_existent_alias(self):
        non_existent_alias = 'unknown'

        disconnect(non_existent_alias)

    @patch.dict('tarantism.connection._connection_settings', {'q': {}})
    @patch.dict('tarantism.connection._connections', {'q': {}})
    @patch.dict('tarantism.connection._spaces', {'q': {}})
    def test_connect_ok(self):
        register_connection(
            self.alias, host=self.host, port=self.port
        )

        space = get_space(self.alias, reconnect=True)
        self.assert_space(space, self.space)
