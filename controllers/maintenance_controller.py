from starlette.requests import Request
from starlette.responses import JSONResponse

from lib import BaseController
from services import MaintenanceService


class MaintenanceController(BaseController):
    
    service = MaintenanceService()
    base_dir = 'maintenance'
    
    async def get(self, request: Request):
        message = self.service.hello_world()
        return self.templates.TemplateResponse(f'{self.base_dir}/maintenance.html', {'request': request, 'message': message})

    async def post(self, request: Request):
        data = await request.json()
        return JSONResponse({'message': data['message']})
