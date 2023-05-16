import multiprocessing

from lib.system_tray_icon import SystemTrayIcon
from app import app


if __name__ == '__main__':
    multiprocessing.freeze_support()
    SystemTrayIcon.start(app)
