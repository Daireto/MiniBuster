from starlette.applications import Starlette
from starlette.routing import Route

from controllers import HomeController, MaintenanceController


def startup():
    print('Ready to start')


def shutdown():
    print('Ready to shutdown')


routes = [
    Route('/', HomeController.home),
    Route('/maintenance', MaintenanceController.maintenance),
]


app = Starlette(
    debug=True,
    routes=routes,
    on_startup=[startup],
    on_shutdown=[shutdown])
