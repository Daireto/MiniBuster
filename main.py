import webbrowser

from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

import env
from controllers import HomeController
from services.database_service import lifespan
from lib.system_tray_icon import SystemTrayIcon


def startup():
    webbrowser.open(f'http://localhost:{env.PORT}')


def shutdown():
    print('Deteniendo la aplicación...')


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
    lifespan=lifespan,
    debug=env.DEBUG,
    routes=routes,
    middleware=middleware,
    on_startup=[startup],
    on_shutdown=[shutdown])


if __name__ == '__main__':
    SystemTrayIcon.start(app)
