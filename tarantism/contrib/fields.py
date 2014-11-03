
import json

from tarantism.fields import BaseField

__all__ = ['JsonField', 'ProtobufField']


class JsonField(BaseField):
    def __init__(self, *args, **kwargs):
        self.dump_kwargs = kwargs.get('dump_kwargs', {})
        self.load_kwargs = kwargs.get('load_kwargs', {})

        super(JsonField, self).__init__(*args, **kwargs)

    def to_db(self, value):
        return json.dumps(value, **self.dump_kwargs)

    def to_python(self, value):
        return json.loads(value, **self.load_kwargs)


class ProtobufField(BaseField):
    def __init__(self, message_class, *args, **kwargs):
        self.message_class = message_class

        super(ProtobufField, self).__init__(*args, **kwargs)

    def to_db(self, value):
        return value.SerializeToString()

    def to_python(self, value):
        message = self.message_class()
        message.ParseFromString(value)

        return message
