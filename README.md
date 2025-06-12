# Api для интернет магазина в соответствии с файлом swagger
___

___
# Основные используемые фреймворки и инструменты

* ### [FastAPI](https://fastapi.tiangolo.com/)
* ### [Pydantic](https://docs.pydantic.dev/latest/)
* ### [Pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
* ### [SQLAlchemy](https://www.sqlalchemy.org/)
* ### [Alembic](https://alembic.sqlalchemy.org/en/latest/)
* ### [Postgres](https://www.postgresql.org/)
* ### [PyJWT](https://pypi.org/project/PyJWT/)
* ### [Bcrypt](https://pypi.org/project/bcrypt/)
* ### [Sqladmin](https://aminalaee.dev/sqladmin/)
* ### [Fastapi-storages](https://aminalaee.dev/fastapi-storages/)
* ### [Fastapi-cache2](https://pypi.org/project/fastapi-cache2/)
* ### [Redis](https://pypi.org/project/redis/)
* ### [Python-json-logger](https://pypi.org/project/python-json-logger/)
* ### [Pytest](https://docs.pytest.org/en/stable/index.html)

## Api:
* Фронтенд находится по адресу http://0.0.0.0:8000/
* Документация API находится по адресу http://0.0.0.0:8000/docs#/
* Административная панель находится по адресу http://0.0.0.0:8000/admin (учетная запись для админа создается автоматически)


## Установка

* Убедитесь, что docker установлен на локальной машине ([Как установить Docker?](https://docs.docker.com/get-started/get-docker/))
* Склонируйте репозиторий на локальную машину
```sh
git clone https://github.com/XXSnape/onlne-store-fastapi.git
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
После регистрации и входа в аккаунт, в cookie записывается JWT-токен, который используется
для авторизации.

## Тестирование
Чтобы запустить тесты, установите зависимости в виртуальное окружение
```sh
pip install poetry && poetry install
```
Запустите скрипт create_certs.py, если нет файлов private.pem и public.pem в директории src/core/certs
```sh
python create_certs.py
```
Создайте файл .env и перенесите туда всё из файла .env_test

Запустите контейнеры с тестовым окружением, чтобы не менять реальные данные
```sh
docker compose -f docker-compose.test.yml up -d
```
Перейдите в директорию tests и запустите тесты
```sh
cd tests && pytest
```


## Данные в .env_template и .env_test

#### DB_HOST - Хост базы данных
#### DB_PORT - Порт базы данных
#### POSTGRES_USER - Логин пользователя 
#### POSTGRES_PASSWORD - Пароль пользователя
#### POSTGRES_DB - Название базы данных

#### REDIS_HOST - Хост редиса

#### SESSION_KEY - Ключ для работы с сессиями

#### ADMIN_NAME - Имя админа
#### ADMIN_LOGIN - Логин админа
#### ADMIN_PASSWORD - Пароль админа

#### LIMIT - Количество загружаемых товаров по умолчанию, для тестов должно быть равно 5
#### TESTING - Параметр, принимающий значение True, если окружение готово к тестированию
