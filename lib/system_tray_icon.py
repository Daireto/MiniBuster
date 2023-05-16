import pystray
import webbrowser
from PIL import Image

from starlette.applications import Starlette

import env
from .server import Server
from .image import mode, size, pixels


class SystemTrayIcon:

    @staticmethod
    def start(app: Starlette):
        image = Image.new(mode=mode, size=size)
        image.putdata(pixels)
        icon = pystray.Icon('MiniBuster', image, menu=pystray.Menu(
            pystray.MenuItem('Abrir', SystemTrayIcon.on_open, default=True),
            pystray.MenuItem('Salir', SystemTrayIcon.on_exit),
        ))
        icon.run(lambda icon: SystemTrayIcon.on_start(icon, app))

    @staticmethod
    def on_start(icon: pystray.Icon, app: Starlette):
        Server.start(app)
        icon.visible = True

    @staticmethod
    def on_open(icon: pystray.Icon, item: pystray._base.MenuItem):
        webbrowser.open(f'http://localhost:{env.PORT}')

    @staticmethod
    def on_exit(icon: pystray.Icon, item: pystray._base.MenuItem):
        Server.stop()
        icon.stop()
