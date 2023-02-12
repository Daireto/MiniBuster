from starlette.requests import Request

from lib import BaseController


class HomeController(BaseController):
    
    async def get(self, request: Request):
        return self.templates.TemplateResponse('index.html', {'request': request})
