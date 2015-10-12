
__all__ = ['QuerySetManager', 'QuerySet']


from tarantism.exceptions import FieldError


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
    def model_class(self):
        return self._model_class

    @property
    def space(self):
        return self._space

    def filter(self, **kwargs):
        values = []
        db_index = None

        index_together = self._model_class._meta.get('index_together', {})

        for field_name in self.model_class._fields_ordered:
            # Silently ignore non defined in model fields
            if field_name not in kwargs:
                continue

            field = self.model_class._fields[field_name]

            value = kwargs[field_name]

            field.validate(value)

            values.append(field.to_python(value))

            if index_together:
                for compound_index_fields, params in index_together.iteritems():
                    if field_name in compound_index_fields:
                        db_index = params.get('db_index', 0)
                        break

            elif field.db_index is not None:
                db_index = field.db_index

        if db_index is None:
            raise FieldError(
                'Index not found for model {model_name} fields {fields}.'.format(
                    model_name=self._model_class.__name__,
                    fields=','.join(kwargs.keys())
                ))

        field_types = self.model_class._get_tarantool_filter_types()

        response = self.space.select(values, index=db_index, field_types=field_types)

        check_tuple_length = self.model_class._meta.get('check_tuple_length', True)

        model_list = []
        model_fields_count = len(self.model_class._fields_ordered)

        for number, values in enumerate(response):
            if check_tuple_length and len(values) != model_fields_count:
                extra_fields = values[model_fields_count:]
                raise FieldError(
                    'Tuple #{number} has {fields_count} extra fields: {fields}'.format(
                        number=number,
                        fields_count=len(extra_fields),
                        fields=','.join(extra_fields)
                    ))

            raw_data = self.model_class._values_to_dict(values)
            model = self.model_class.from_dict(raw_data)
            model._exists_in_db = True
            model_list.append(model)

        return model_list

    def get(self, **kwargs):
        model_list = self.filter(**kwargs)
        if not model_list:
            raise self.model_class.DoesNotExist(
                '{model_class} instance does not exists.'.format(
                    model_class=self.model_class
                ))
        elif len(model_list) > 1:
            raise self.model_class.MultipleObjectsReturned(
                'get() returned more than one {model_class} '
                '-- it returned {count}!'.format(
                    model_class=self.model_class, count=len(model_list)
                )
            )

        return model_list[0]

    def create(self, **kwargs):
        return self.model_class(**kwargs).save()

    def delete(self, **kwargs):
        values = []
        for field_name in self.model_class._fields_ordered:
            field = self.model_class._fields[field_name]
            if field_name in kwargs:
                values.append(field.to_python(kwargs[field_name]))

        response = self.space.delete(values)

        return response.rowcount > 0
