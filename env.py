# Application
NAME = 'MiniBuster'
DEBUG = True

# Server
APP = 'main:app'
HOST = '0.0.0.0'
PORT = 8010
LOG_LEVEL = 'info'
RELOAD = True

#database
DATABASE_URL = 'sqlite:///'

# Maintenance
DEFAULT_CONFIG = {
    "system": {
        "temp_files": True,
        "recycle_bin": False
    },
    "browsers": {
        "chrome": {
            "history": True,
            "cache": True,
            "cookies": True,
            "extensions": False,
            "passwords": True
        },
        "opera": {
            "history": True,
            "cache": True,
            "cookies": True,
            "extensions": False,
            "passwords": True
        },
        "edge": {
            "history": True,
            "cache": True,
            "cookies": True,
            "extensions": False,
            "passwords": True
        }
    }
}
