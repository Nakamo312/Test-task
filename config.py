import os

from dotenv import load_dotenv

load_dotenv()
NAME = os.environ.get("NAME")
HOST = os.environ.get("HOST")
PORT = int(os.environ.get("PORT"))

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
DB_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

APACHE_HOST = os.environ.get("APACHE_HOST")
APACHE_PORT = os.environ.get("APACHE_PORT")
APACHE_SERVER = f'{APACHE_HOST}:{APACHE_PORT}'