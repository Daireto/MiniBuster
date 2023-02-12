import uvicorn
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

import env

from controllers import HomeController, MaintenanceController


def startup():
    print(f'Application is running on port {env.PORT}')


def shutdown():
    print('Shutting down application...')


routes = [
    Route('/', HomeController),
    Route('/maintenance', MaintenanceController),
    Mount('/static', app=StaticFiles(directory='static'), name="static"),
]


app = Starlette(
    debug=env.DEBUG,
    routes=routes,
    on_startup=[startup],
    on_shutdown=[shutdown])

if __name__ == '__main__':
    uvicorn.run(
        app=env.APP,
        host=env.HOST,
        port=env.PORT,
        log_level=env.LOG_LEVEL,
        reload=env.RELOAD)
