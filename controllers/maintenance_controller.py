from starlette.requests import Request
from starlette.responses import JSONResponse

from lib import BaseController
from services import MaintenanceService


class MaintenanceController(BaseController):
    
    service = MaintenanceService()
    
    async def get(self, request: Request):
        await self.service.delete_history_chrome()
        return JSONResponse({'message': 'Clear successfully'})

    async def post(self, request: Request):
        data = await self.service.clear_temp()
        return JSONResponse({'message': 'Clear successfully'})
