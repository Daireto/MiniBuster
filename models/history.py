import sqlalchemy

from lib.base_database import BaseDatabase
from .configuration import Configuration


class History(BaseDatabase):
    __tablename__ = 'history'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_configuration = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(Configuration.id))
    deleted = sqlalchemy.Column(sqlalchemy.Integer)
    state = sqlalchemy.Column(sqlalchemy.Boolean)
    message_error = sqlalchemy.Column(sqlalchemy.String)
    date = sqlalchemy.Column(sqlalchemy.String)