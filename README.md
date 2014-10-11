# Tarantism

## О проекте

Tarantism - это минималистичный ORM для NOSQL базы данных [Tarantool](http://tarantool.org/).

[![Build Status](https://travis-ci.org/marrrvin/tarantism.svg?branch=master)](https://travis-ci.org/marrrvin/tarantism)

## Пример использования

```python
from tarantism import connect
from tarantism import models


class User(models.Model):
    pk = models.LongField()
    age = models.IntField(
        verbose_name=u'Age'
    )
    login = models.StringField(
        max_length=10,
        max_length=50,
        verbose_name=u'Login'
    )
    password = models.StringField(
        max_length=6,
        max_length=20,
        verbose_name=u'Password'
    )
    bio = models.StringField(
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

user.update(bio=u'User bio.', age__add=1)

user.delete()
```
