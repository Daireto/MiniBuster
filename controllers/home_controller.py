from starlette.requests import Request
from starlette.templating import _TemplateResponse

from lib import BaseController
import env


class HomeController(BaseController):
    
    base_dir = 'home'
    
    @classmethod
    async def home_page(cls, request: Request) -> _TemplateResponse:
        return cls.templates.TemplateResponse(f'{cls.base_dir}/index.html', {'request': request, 'appName': env.NAME})
