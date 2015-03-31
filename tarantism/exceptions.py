
__all__ = [
    'DoesNotExist',
    'MultipleObjectsReturned',
    'ValidationError',
    'FieldError'
]


class DoesNotExist(Exception):
    pass


class MultipleObjectsReturned(Exception):
    pass


class ValidationError(Exception):
    pass


class FieldError(Exception):
    pass
