# Api для интернет магазина в соответствии с файлом swagger
___

___
# Основные используемые фреймворки и инструменты

* ### [FastAPI](https://fastapi.tiangolo.com/)
* ### [Pydantic](https://docs.pydantic.dev/latest/)
* ### [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
* ### [SQLAlchemy](https://www.sqlalchemy.org/)
* ### [Alembic](https://alembic.sqlalchemy.org/en/latest/)
* ### [Postgres](https://www.postgresql.org/)
* ### [PyJWT](https://pypi.org/project/PyJWT/)
* ### [bcrypt](https://pypi.org/project/bcrypt/)
* ### [sqladmin](https://aminalaee.dev/sqladmin/)
* ### [fastapi-storages](https://aminalaee.dev/fastapi-storages/)
* ### [fastapi-cache2](https://pypi.org/project/fastapi-cache2/)
* ### [aioredis](https://aioredis.readthedocs.io/en/latest/)
* ### [python-json-logger](https://pypi.org/project/python-json-logger/)

## Api:
* Фронтенд находится по адресу http://0.0.0.0:8000/
* Документация API находится по адресу http://0.0.0.0:8000/docs#/
* Административная панель находится по адресу http://0.0.0.0:8000/admin (учетная запись для админа создается автоматически)


## Установка

* Убедитесь, что docker установлен на локальной машине ([Как установить Docker?](https://docs.docker.com/get-started/get-docker/))
* Склонируйте репозиторий на локальную машину
```sh
https://github.com/raydqver/onlne-store-fastapi.git
```

* Создайте файл .env co своими данными и скопируйте все из .env_template,
либо введите свои данные

* Запустите докер контейнер и подождите около 2 минут
```sh
docker compose up
```

## CERTS
В данной директории хранятся файлы private.pem и public.pem с 
закрытым и открытым ключами соответственно для шифрования JWT-токенов. 
Они генерируются автоматически запуском скрипта create_certs.py внутри докера.

## Данные в .env_template

#### DB_HOST - Хост базы данных
#### DB_PORT - Порт базы данных
#### POSTGRES_USER - Логин пользователя 
#### POSTGRES_PASSWORD - Пароль пользователя
#### POSTGRES_DB - Название базы данных

#### REDIS_HOST - Хост редиса

#### SESSION_KEY - Ключ для работы с сессиями

#### ADMIN_NAME - Имя админа
#### ADMIN_LOGIN - Логин админа
#### ADMIN_PASSWORD - Логин пароль админа

