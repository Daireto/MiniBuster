import platform
import webbrowser
import env
import os

from datetime import datetime
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from controllers import HomeController, MaintenanceController
from services import DatabaseService, UserService
from lib.system_tray_icon import SystemTrayIcon

database_service = DatabaseService()
user_service = UserService()

async def startup():
    webbrowser.open(f'http://localhost:{env.PORT}')
    await database_service.connect()
    await user_service.set_user({'id': 1, 'name': os.getenv('username'), 'last_session': datetime.now(), 'os': platform.system(), 'device': platform.node()})

async def shutdown():
    await database_service.disconnect()

routes = [
    Route('/', HomeController.home_page, methods=['GET']),
    Route('/maintenance', MaintenanceController.main_page, methods=['GET']),
    Route('/maintenance', MaintenanceController.submit, methods=['POST']),
    Route('/maintenance/get_resources', MaintenanceController.get_resources, methods=['GET']),
    Mount('/static', app=StaticFiles(directory='static'), name="static"),
]


middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'])
]


app = Starlette(
    on_startup=[startup],
    on_shutdown=[shutdown],
    debug=env.DEBUG,
    routes=routes,
    middleware=middleware)


if __name__ == '__main__':
    SystemTrayIcon.start(app)
