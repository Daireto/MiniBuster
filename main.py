import uvicorn
import webbrowser

from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.middleware import Msiddleware
from starlette.middleware.cors import CORSMiddleware

import env

from controllers import HomeController, BrowsersController, ResourceController, ClearController


def startup():
    print(f'Application is running on port {env.PORT}')
    # webbrowser.open(f'http://localhost:{env.PORT}') // TODO: Active when done project


def shutdown():
    print('Shutting down application...')


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
    debug=env.DEBUG,
    routes=routes,
    middleware=middleware,
    on_startup=[startup],
    on_shutdown=[shutdown])

if __name__ == '__main__':
    uvicorn.run(
        app=env.APP,
        host=env.HOST,
        port=env.PORT,
        log_level=env.LOG_LEVEL,
        reload=env.RELOAD)
