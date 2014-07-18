
import tarantool


spaces = {}


DEFAULT_ALIAS = 'default'


def initialize(alias=DEFAULT_ALIAS, **kwargs):
    global spaces

    space_num = kwargs.pop('space')

    server = tarantool.connect(**kwargs)
    space = server.space(space_num)
    spaces[alias] = space

    return space
