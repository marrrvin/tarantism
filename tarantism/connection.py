
import tarantool


__all__ = [
    'DEFAULT_ALIAS', 'DEFAULT_SETTINGS',
    'register_connection', 'get_connection',
    'disconnect', 'get_space', 'connect'
]


_connection_settings = {}
_connections = {}
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
            raise ValueError(
                'Connection with alias {alias} have not defined.'.format(
                    alias=alias
                )
            )

        _connections[alias] = tarantool.connect(
            host=conn_settings.get('host'),
            port=conn_settings.get('port')
        )

    return _connections[alias]


def disconnect(alias=DEFAULT_ALIAS):
    global _connections
    global _spaces

    if alias in _connections:
        get_connection(alias=alias).close()
        del _connections[alias]

    if alias in _spaces:
        del _spaces[alias]


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
