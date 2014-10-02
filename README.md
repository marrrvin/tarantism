# Tarantism

## О проекте

Tarantism - это минималистичный ORM поверх NOSQL базы данных [Tarantool](http://tarantool.org/).

## Пример использования

```python
from tarantism import connect
from tarantism import Model
from tarantism import LongField
from tarantism import IntegerField
from tarantism import StringField


class User(Model):
    pk = LongField()
    age = IntField(
        verbose_name=u'Age'
    )
    login = StringField(
        max_length=10,
        max_length=50,
        verbose_name=u'Login'
    )
    password = StringField(
        max_length=6,
        max_length=20,
        verbose_name=u'Password'
    )
    bio = StringField(
        required=False,
        verbose_name=u'User biography'
    )

connect()


user = User(
    pk=1L,
    age=27,
    login=u'the_login',
    password=u'********'
)
user.save()

user.bio = u'Good guy.'

user.update()

user.delete()
```
