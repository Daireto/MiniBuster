import sqlalchemy

from lib.base_database import BaseDatabase


class User(BaseDatabase):
    __tablename__ = 'user'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    last_session = sqlalchemy.Column(sqlalchemy.String)
    os = sqlalchemy.Column(sqlalchemy.String)
    device = sqlalchemy.Column(sqlalchemy.String)
