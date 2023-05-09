import contextlib
import env
import databases
import sqlalchemy

from starlette.responses import JSONResponse
from sqlalchemy_utils import database_exists

from lib import BaseService


DATABASE_URL = env.DATABASE_URL

metadata = sqlalchemy.MetaData()

configuration = sqlalchemy.Table(
    "configuration",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("id_user", sqlalchemy.Integer, sqlalchemy.ForeignKey('user.id')),
    sqlalchemy.Column("active", sqlalchemy.Boolean),
    sqlalchemy.Column("clean_recycle_bin", sqlalchemy.Boolean),
    sqlalchemy.Column("clean_temp", sqlalchemy.Boolean),
    sqlalchemy.Column("clean_browsers", sqlalchemy.Boolean),
)

history = sqlalchemy.Table(
    "history",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("id_configuration", sqlalchemy.String, sqlalchemy.ForeignKey('configuration.id')),
    sqlalchemy.Column("deleted", sqlalchemy.String),
    sqlalchemy.Column("state", sqlalchemy.String),
    sqlalchemy.Column("message_error", sqlalchemy.String),
    sqlalchemy.Column("date", sqlalchemy.Boolean),
)

user = sqlalchemy.Table(
    "user",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("last_session", sqlalchemy.String),
    sqlalchemy.Column("so", sqlalchemy.String),
    sqlalchemy.Column("device", sqlalchemy.String),
)

database = databases.Database(DATABASE_URL)

@contextlib.asynccontextmanager
async def lifespan(app):
    if not database_exists(DATABASE_URL):
        engine = sqlalchemy.create_engine('sqlite:///C:\\sqlitedbs\\minibuster.db', echo=True)
        with engine.connect() as conn:
            pass
    await database.connect()
    yield
    await database.disconnect()


class DatabaseService(BaseService):
    async def get_configurations(request) -> JSONResponse:
        try:
            query = configuration.select()
            results = await database.fetch_all(query)
            content = [
                {
                    "id": result["id"],
                    "id_user": result["id_user"],
                    "active": result["active"],
                    "clean_recycle_bin": result["clean_recycle_bin"],
                    "clean_temp": result["clean_temp"],
                    "clean_browsers": result["clean_browsers"]
                }
                for result in results
            ]
            return JSONResponse(content)
        except Exception as error:
            return JSONResponse({}, 400)

    async def set_configuration(request) -> JSONResponse:
        try:
            data = await request.json()
            query = configuration.insert().values(
                id=data["id"],
                id_user=data["id_user"],
                active=data["active"],
                clean_recycle_bin=data["clean_recycle_bin"],
                clean_temp=data["clean_temp"],
                clean_browsers=data["clean_browsers"]
            )
            await database.execute(query)
            return JSONResponse({}, 200)
        except Exception as error:
            return JSONResponse({}, 400)

    async def get_history(request) -> JSONResponse:
        try:
            query = history.select()
            results = await database.fetch_all(query)
            content = [
                {
                    "id": result["id"],
                    "id_configuration": result["id_configuration"],
                    "deleted": result["deleted"],
                    "state": result["state"],
                    "message_error": result["message_error"],
                    "date": result["date"]
                }
                for result in results
            ]
            return JSONResponse(content)
        except Exception as error:
            return JSONResponse({}, 400)

    async def set_history(request) -> JSONResponse:
        try:
            data = await request.json()
            query = history.insert().values(
                id=data["id"],
                id_configuration=data["id_configuration"],
                deleted=data["deleted"],
                state=data["state"],
                message_error=data["message_error"],
                date=data["date"]
            )
            await database.execute(query)
            return JSONResponse({}, 200)
        except Exception as error:
            return JSONResponse({}, 400)

    async def get_user(request) -> JSONResponse:
        try:
            query = user.select()
            results = await database.fetch_all(query)
            content = [
                {
                    "id": result["id"],
                    "name": result["name"],
                    "last_session": result["last_session"],
                    "so": result["so"],
                    "device": result["device"]
                }
                for result in results
            ]
            return JSONResponse(content)
        except Exception as error:
            return JSONResponse({}, 400)

    async def set_user(request) -> JSONResponse:
        try:
            data = await request.json()
            query = user.insert().values(
                id=data["id"],
                name=data["name"],
                last_session=data["last_session"],
                so=data["so"],
                device=data["device"]
            )
            await database.execute(query)
            return JSONResponse({}, 200)
        except Exception as error:
            return JSONResponse({}, 400)
