
import json

from tarantism.fields import BaseField


class JsonField(BaseField):
    def __init__(self, *args, **kwargs):
        self.dump_kwargs = kwargs.get('dump_kwargs', {})
        self.load_kwargs = kwargs.get('load_kwargs', {})

        super(JsonField, self).__init__(*args, **kwargs)

    def to_db(self, value):
        return json.dumps(value, **self.dump_kwargs)

    def to_python(self, value):
        return json.loads(value, **self.load_kwargs)
