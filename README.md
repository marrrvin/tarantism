# Tarantism

```

## О проекте

Tarantism - это минималистичный ORM поверх NOSQL базы данных [Tarantool](http://tarantool.org/).

## Пример использования

```
class User(Model):
    pk = LongField()
    age = IntegerField(
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
```
