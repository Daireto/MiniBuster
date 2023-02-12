from lib import BaseController
from services import MaintenanceService


class MaintenanceController(BaseController):
    
    @classmethod
    def maintenance(cls, request):
        message = MaintenanceService.hello_world()
        return cls.templates.TemplateResponse('index.html', {'request': request, 'message': message})
