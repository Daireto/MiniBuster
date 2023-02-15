from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

from lib import BaseController
from services import MaintenanceService

class BrowsersController(BaseController):

    service = MaintenanceService()

    async def get(self, request: Request):
        response = request.json()
        response = await run_in_threadpool(self.service.delete_history_chrome)
        return JSONResponse({'message': 'Clear browser successfully'})


class ClearController(BaseController):

    service = MaintenanceService()

    async def get(self, request: Request):
        response = request.json()
        response = await run_in_threadpool(self.service.clear_temp)
        return JSONResponse({'message': 'Clear browser successfully'})


class ResourceController(BaseController):

    service = MaintenanceService()

    async def get(self, request: Request):
        response = await run_in_threadpool(self.service.get_resources)
        print(response)
        return JSONResponse(response)
