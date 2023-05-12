from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.templating import _TemplateResponse

from lib import BaseController
from services import MaintenanceService


class MaintenanceController(BaseController):

    service = MaintenanceService()
    base_dir = 'maintenance'

    @classmethod
    async def main_page(cls, request: Request) -> _TemplateResponse:
        return cls.templates.TemplateResponse(f'{cls.base_dir}/maintenance.html', {'request': request})

    @classmethod
    async def get_config(cls, request: Request) -> JSONResponse:
        return JSONResponse(cls.service.get_config())

    @classmethod
    async def get_resources(cls, request: Request) -> JSONResponse:
        return JSONResponse(cls.service.get_resources())

    @classmethod
    async def submit(cls, request: Request) -> JSONResponse:
        data = await request.json()
        response = cls.service.execute_maintenance(data)
        return JSONResponse({'data': response})
