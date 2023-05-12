import sqlalchemy

from lib.base_database import BaseDatabase
from .configuration import Configuration


class History(BaseDatabase):
    __tablename__ = 'history'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    id_configuration = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(Configuration.id))
    deleted = sqlalchemy.Column(sqlalchemy.String)
    state = sqlalchemy.Column(sqlalchemy.String)
    message_error = sqlalchemy.Column(sqlalchemy.String)
    date = sqlalchemy.Column(sqlalchemy.Boolean)