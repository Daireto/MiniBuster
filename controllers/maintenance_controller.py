from typing import Any

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException
from starlette.templating import _TemplateResponse

from lib import BaseController
from services.maintenance_service import BrowsersConfig, MaintenanceService, Config


class MaintenanceController(BaseController):

    service = MaintenanceService()
    base_dir = 'maintenance'

    @classmethod
    def __get_config(cls, data: dict[str, Any]):
        try:
            return Config(
                system=data['system'],
                browsers=BrowsersConfig(
                    chrome=data['browsers']['chrome'],
                    edge=data['browsers']['edge'],
                    opera=data['browsers']['opera'],
                )
            )
        except:
            raise HTTPException(400, 'Configuración no válida')

    @classmethod
    async def main_page(cls, request: Request) -> _TemplateResponse:
        return cls.templates.TemplateResponse(f'{cls.base_dir}/maintenance.html', {'request': request})

    @classmethod
    async def get_config(cls, request: Request) -> JSONResponse:
        return JSONResponse(await cls.service.get_config())

    @classmethod
    async def get_resources(cls, request: Request) -> JSONResponse:
        return JSONResponse(cls.service.get_resources())

    @classmethod
    async def submit(cls, request: Request) -> JSONResponse:
        data = await request.json()
        response = await cls.service.execute_maintenance(cls.__get_config(data))
        return JSONResponse({'data': response})
