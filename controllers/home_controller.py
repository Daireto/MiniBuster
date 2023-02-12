from lib import BaseController


class HomeController(BaseController):
    
    @classmethod
    def home(cls, request):
        return cls.templates.TemplateResponse('index.html', {'request': request})
