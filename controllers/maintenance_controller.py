from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

from lib import BaseController
from services import MaintenanceService


class MaintenanceController(BaseController):

    service = MaintenanceService    ()

    async def get(self, request: Request):
        response = await run_in_threadpool(self.service.delete_history_chrome)
        return JSONResponse({'message': 'Clear browser successfully'})

    async def post(self, request: Request):
        response = await run_in_threadpool(self.service.clear_temp)
        print(response)
        return JSONResponse({'message': 'Clear cache successfully'})
