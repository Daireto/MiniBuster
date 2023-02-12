from starlette.requests import Request
from starlette.responses import JSONResponse

from lib import BaseController
from services import MaintenanceService


class MaintenanceController(BaseController):
    
    service = MaintenanceService()
    
    async def get(self, request: Request):
        message = self.service.hello_world()
        return self.templates.TemplateResponse('index.html', {'request': request, 'message': message})

    async def post(self, request: Request):
        data = await self.service.clear_temp()
        return JSONResponse({'message': 'Clear successfully'})
