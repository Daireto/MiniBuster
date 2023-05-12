import os
import env
import databases

from sqlalchemy_utils import database_exists, create_database

from lib import BaseService
from lib.base_database import BaseDatabase, engine


class DatabaseService(BaseService):

    __database_url = env.DATABASE_URL + fr"C:\Users\{os.getenv('username')}" + r"\minibuster.db"

    database = databases.Database(__database_url)

    async def __create_dtb(self):
        url = self.__database_url
        if not database_exists(url):
            create_database(url)
            BaseDatabase.metadata.create_all(engine)

    async def connect(self):
        await self.__create_dtb()
        await self.database.connect()

    async def disconnect(self):
        await self.database.disconnect()
