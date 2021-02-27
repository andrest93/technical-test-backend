import peewee as pw
import datetime

DATA_BASE_NAME = 'notes.db'

data_base = pw.SqliteDatabase(DATA_BASE_NAME)

class BaseModel(pw.Model):

    class Meta:
        database = data_base


class User(BaseModel):
    user = pw.CharField(unique=True)
    password = pw.CharField()

    class Meta:
        db_table = 'users'


class Note(BaseModel):
    text = pw.CharField()
    created_at = pw.DateTimeField(default=datetime.datetime.now)
    user = pw.ForeignKeyField(User)

    class Meta:
        db_table = 'notes'


def create_tables():
    Note.create_table(True)
    User.create_table(True)


create_tables()
