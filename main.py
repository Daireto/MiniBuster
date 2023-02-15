import uvicorn
import webbrowser

from starlette.applications import Starlette
from starlette.routing import Route

import env

from controllers import HomeController, BrowsersController, ResourceController, ClearController


def startup():
    print(f'Application is running on port {env.PORT}')
    # webbrowser.open(f'http://localhost:{env.PORT}') // TODO: Active when done project


def shutdown():
    print('Shutting down application...')


routes = [
    Route('/', HomeController),
    Route('/maintenance/delete_history_chrome', BrowsersController),
    Route('/maintenance/clear_temp', ClearController),
    Route('/maintenance/resources/', ResourceController),
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
