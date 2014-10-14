
import json

from tarantism.fields import BaseField


class JsonField(BaseField):
    @property
    def python_type(self):
        return unicode

    def to_db(self, value):
        return json.dumps(value)

    def to_python(self, value):
        return json.loads(value)
