
__all__ = ['QuerySetManager', 'QuerySet']

DEFAULT_PRIMARY_KEY_FIELD_NAME = 'pk'

DEFAULT_INDEX_NO = 0


class QuerySetManager(object):
    def __get__(self, instance, owner):
        if instance is not None:
            return self

        return QuerySet(owner, owner.get_space())


class QuerySet(object):
    def __init__(self, model_class, space):
        self._model_class = model_class
        self._space = space

    @property
    def space(self):
        return self._space

    def filter(self, **kwargs):
        field_name, value = kwargs.items().pop()

        index = self._get_index_number_by_field_name(field_name)

        field_types = self._model_class._get_tarantool_types()
        response = self.space.select(value, index=index, field_types=field_types)

        model_list = []
        for values in response:
            raw_data = self._model_class._values_to_dict(values)
            model_list.append(self._model_class._model_from_data(raw_data))

        return model_list

    def get(self, **kwargs):
        model_list = self.filter(**kwargs)

        if not model_list:
            raise self._model_class.DoesNotExist(
                '{model_class} instance does not exists.'.format(
                    model_class=self._model_class
                ))
        elif len(model_list) > 1:
            raise self._model_class.MultipleObjectsReturned(
                'get() returned more than one {model_class} '
                '-- it returned {count}!'.format(
                    model_class=self._model_class, count=len(model_list)
                )
            )

        return model_list.pop()

    def create(self, **kwargs):
        return self._model_class(**kwargs).save()

    def _get_index_number_by_field_name(self, field_name):
        if field_name not in self._model_class._fields:
            raise ValueError(
                'Field {name} is not in defined field list: '
                '[{field_list}].'.format(
                    name=field_name,
                    field_list=', '.join(self._model_class._fields_ordered)
                )
            )

        field = self._model_class._fields[field_name]
        if field.db_index is not None:
            return field.db_index

        if field_name == DEFAULT_PRIMARY_KEY_FIELD_NAME:
            return DEFAULT_INDEX_NO

        raise ValueError(
            'Field {name} is not marked as indexed.'.format(name=field_name)
        )
