from multiprocessing import Process
import subprocess
import psutil

import uvicorn
from starlette.applications import Starlette

import env


class Server:

    app: Starlette
    proc: Process
    pid: int | None

    @staticmethod
    def start(app: Starlette):
        Server.app = app
        Server.proc = Process(target=uvicorn.run,
            args=(),
            kwargs={
                'app': env.APP,
                'host': env.HOST,
                'port': env.PORT,
                'log_level': env.LOG_LEVEL,
                'reload': env.RELOAD},
            daemon=False)
        Server.proc.start()

    @staticmethod
    def stop():
        if not Server.proc.is_alive() or not Server.proc.pid:
            return
        parent = psutil.Process(Server.proc.pid)
        for child in parent.children(recursive=True):
            child.kill()
        parent.kill()
        try:
            Server.proc.terminate()
            Server.proc.kill()
        except:
            print('El proceso ha sido detenido')
