
import tarantool


__all__ = ['connect', 'register_connection', 'get_space',
           'DEFAULT_ALIAS', 'DEFAULT_SETTINGS']


_connections = {}

_connection_settings = {}

_spaces = {}


DEFAULT_ALIAS = 'default'

DEFAULT_SETTINGS = {
    'host': 'localhost',
    'port': 33013,
    'space': 0
}


def register_connection(alias, **kwargs):
    global _connection_settings

    conn_settings = DEFAULT_SETTINGS.copy()
    conn_settings.update(kwargs)

    _connection_settings[alias] = conn_settings


def get_connection(alias=DEFAULT_ALIAS, reconnect=False):
    global _connections

    if reconnect:
        disconnect(alias)

    if alias not in _connections:
        conn_settings = _connection_settings.get(alias)

        if not _connection_settings:
            raise ValueError('Connection with alias {alias} have not defined.')

        _connections[alias] = tarantool.connect(
            host=conn_settings.get('host'),
            port=conn_settings.get('port')
        )

    return _connections[alias]


def disconnect(alias=DEFAULT_ALIAS):
    global _connections

    if alias in _connections:
        get_connection(alias=alias).disconnect()
        del _connections[alias]


def get_space(alias=DEFAULT_ALIAS, reconnect=False):
    global _spaces

    if reconnect:
        disconnect(alias)

    if alias not in _spaces:
        conn = get_connection(alias)
        conn_settings = _connection_settings[alias]

        _spaces[alias] = conn.space(conn_settings['space'])

    return _spaces[alias]


def connect(space, alias=DEFAULT_ALIAS, **kwargs):
    global _connections

    if alias not in _connections:
        register_connection(alias, space, **kwargs)

    return get_connection(alias, **kwargs)
