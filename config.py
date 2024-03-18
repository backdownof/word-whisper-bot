import os

from aiogram import Bot
from dotenv import load_dotenv

load_dotenv()


class App:
    __conf = {
        'BOT_TOKEN': os.getenv('BOT_TOKEN'),

        'ENV': os.getenv('SERVER_SOFTWARE'),

        'REDIS_HOST': os.getenv('REDIS_HOST'),
        'REDIS_PORT': os.getenv('REDIS_PORT'),
        'REDIS_PASS': os.getenv('REDIS_PASS'),
        'REDIS_EXPOSED_PORT': os.getenv('REDIS_EXPOSED_PORT'),

        'CELERY_HOST': os.getenv('CELERY_HOST'),

        'PG_USER': os.getenv('PG_USER'),
        'PG_PASS': os.getenv('PG_PASS'),
        'PG_HOST': os.getenv('PG_HOST'),
        'PG_PORT': os.getenv('PG_PORT'),
        'PG_DB_NAME': os.getenv('PG_DB_NAME'),
        'PG_EXPOSED_PORT': os.getenv('PG_EXPOSED_PORT'),
    }
    __setters = []

    @staticmethod
    def config(name):
        if name == 'REDIS_URI':
            return App.__get_redis_uri()
        elif name == 'POSTGRES_URI':
            return App.__get_postgres_uri()
        return App.__conf[name]

    @staticmethod
    def set(name, value):
        if name in App.__setters:
            App.__conf[name] = value
        else:
            raise NameError("Name not accepted in set() method")

    @staticmethod
    def __get_redis_uri():
        host = App.config('REDIS_HOST')
        port = App.config('REDIS_PORT')
        password = App.config('REDIS_PASS')

        return f'redis://default:{password}@{host}:{port}'
        # return f'redis://default:{password}@localhost:{port}'

    @staticmethod
    def __get_postgres_uri():
        host = App.config('PG_HOST')
        port = App.config('PG_PORT')
        db_name = App.config('PG_DB_NAME')
        user = App.config('PG_USER')
        password = App.config('PG_PASS')
        exposed_port = App.config('PG_EXPOSED_PORT')

        return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
        # return f"postgresql://{user}:{password}@localhost:{port}/{db_name}"

    @staticmethod
    def bot():
        return Bot(token=App.config('BOT_TOKEN'))
