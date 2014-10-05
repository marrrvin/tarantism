
__all__ = [
    'DoesNotExist',
    'MultipleObjectsReturned',
    'ImproperlyConfigured',
    'ValidationError'
]


class DoesNotExist(Exception):
    pass


class MultipleObjectsReturned(Exception):
    pass


class ImproperlyConfigured(Exception):
    pass


class ValidationError(Exception):
    pass
