from starlette.requests import Request

from lib import BaseController
import env


class HomeController(BaseController):
    
    base_dir = 'home'
    
    async def get(self, request: Request):
        return self.templates.TemplateResponse(f'{self.base_dir}/index.html', {'request': request, 'appName': env.NAME})
