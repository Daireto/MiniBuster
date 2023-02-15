import psutil, os

from lib import BaseService


class MaintenanceService(BaseService):
    
    def hello_world(self):
        return "Hello, World!"

    def get_resources(self) -> dict[str, float]:
        return {
            'cpu': psutil.cpu_percent(),
            'memory': psutil.virtual_memory().percent,
            'disk': psutil.disk_usage(os.getcwd()).percent
        }
