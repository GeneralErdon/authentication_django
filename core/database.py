from pathlib import Path
from apps.base.utils import MessageManager as MM
import os

class enumDB:
    POSTGRES = 'postgresql'
    MYSQL = 'mysql'


def get_db_config(db_engine:str = "sqlite", sqlite_path:Path = Path(__file__).resolve().parent.parent) -> dict[str, str]:
    if db_engine == enumDB.POSTGRES:
        return {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':     os.environ.get('DBNAME'),
        'USER':     os.environ.get('DBUSER'),
        'PASSWORD': os.environ.get('DBPASSWORD'),
        'PORT':     os.environ.get('DBPORT'),
        'HOST':     os.environ.get('DBHOST'),
    }
    elif db_engine == enumDB.MYSQL:
        return {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':     os.environ.get('DBNAME'),
        'USER':     os.environ.get('DBUSER'),
        'PASSWORD': os.environ.get('DBPASSWORD'),
        'PORT':     os.environ.get('DBPORT'),
        'HOST':     os.environ.get('DBHOST'),
    }
    else:
        MM.warning("Se está usando SQLITE por defecto," + 
                " recuerda establecer las variables de entorno")
        return {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': sqlite_path / 'db.sqlite3',
    }