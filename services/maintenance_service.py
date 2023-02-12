from lib import BaseService


class MaintenanceService(BaseService):
    
    @classmethod
    def hello_world(cls):
        return "Hello, World!"
