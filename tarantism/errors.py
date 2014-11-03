
__all__ = [
    'DoesNotExist',
    'MultipleObjectsReturned',
    'ValidationError'
]


class DoesNotExist(Exception):
    pass


class MultipleObjectsReturned(Exception):
    pass


class ValidationError(Exception):
    pass
