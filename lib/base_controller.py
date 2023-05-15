from starlette.endpoints import HTTPEndpoint
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import Response

import env


class BaseController(HTTPEndpoint):

    templates = Jinja2Templates(directory=env.TEMPLATES_URL)

    async def get(self, request: Request) -> Response:
        return Response()

    async def post(self, request: Request) -> Response:
        return Response()
