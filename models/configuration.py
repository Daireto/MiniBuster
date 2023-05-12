import sqlalchemy

from lib.base_database import BaseDatabase
from .user import User


class Configuration(BaseDatabase):
    __tablename__ = 'configuration'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    id_user = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(User.id))
    active = sqlalchemy.Column(sqlalchemy.Boolean)
    clean_recycle_bin = sqlalchemy.Column(sqlalchemy.Boolean)
    clean_temp = sqlalchemy.Column(sqlalchemy.Boolean)
    clean_browsers = sqlalchemy.Column(sqlalchemy.PickleType)