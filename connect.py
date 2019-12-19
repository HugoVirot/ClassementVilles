from peewee import *

sqlite_db = SqliteDatabase('cities_ranking.db', pragmas={'journal_mode': 'wal'})
