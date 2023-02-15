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
        message = cls.service.hello_world()
        return cls.templates.TemplateResponse(f'{cls.base_dir}/maintenance.html', {'request': request, 'message': message})
    
    @classmethod
    async def get_resources(cls, request: Request) -> JSONResponse:
        return JSONResponse(cls.service.get_resources())

    @classmethod
    async def submit(cls, request: Request) -> JSONResponse:
        data = await request.json()
        return JSONResponse({'message': data['message']})
