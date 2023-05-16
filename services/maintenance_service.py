from datetime import datetime
import json
import os
import typing
import psutil
import subprocess
from dataclasses import asdict, dataclass

from lib import BaseService
from services.configuration_service import ConfigurationService
from services.history_service import HistoryService

import env


@dataclass
class BrowsersConfig:
    chrome: dict[str, bool]
    opera: dict[str, bool]
    edge: dict[str, bool]


@dataclass
class Config:
    system: dict[str, bool]
    browsers: BrowsersConfig


@dataclass
class OperationResult:
    deletedFiles: list[str]
    deleted: int
    skipped: int


@dataclass
class MaintenanceResponse:
    temp_files: OperationResult
    recycle_bin: OperationResult
    browsers: OperationResult
    deleted: int
    skipped: int


class MaintenanceService(BaseService):

    __configuration_service = ConfigurationService()

    __history_service = HistoryService()

    __browsers_options = {
        'history': {
            'chrome': '"History", "Service Worker", "Top Sites", "Visited Links", "Web Data"',
            'opera': '"History", "Service Worker", "Top Sites", "Visited Links", "Web Data"',
            'edge': '"History", "Service Worker", "Top Sites", "Visited Links", "Web Data"'
        },
        'cache': {
            'chrome': r'"Cache", "Cache2\entries\", "ChromeDWriteFontCache", "Code Cache", "GPUCache", "JumpListIcons", "JumpListIconsOld", "JumpListIconsRecentClosed", "Media Cache"',
            'opera': r'"Cache", "Cache2\entries\", "Code Cache", "GPUCache", "JumpListIcons", "JumpListIconsOld", "JumpListIconsRecentClosed", "Media Cache"',
            'edge': r'"Cache", "Cache2\entries\", "Code Cache", "GPUCache", "JumpListIcons", "JumpListIconsOld", "JumpListIconsRecentClosed", "Media Cache"'
        },
        'cookies': {
            'chrome': '"Cookies"',
            'opera': '"Cookies"',
            'edge': '"Cookies"'
        },
        'extensions': {
            'chrome': '"Extensions"',
            'opera': '"Extensions"',
            'edge': '"Extensions"'
        },
        'passwords': {
            'chrome': '"Login Data"',
            'opera': '"Login Data"',
            'edge': '"Login Data"'
        }
    }

    __username = os.getenv('username')

    __initial_command = """
        $items = 0;
        $disco = 'C';
        $tempFolders = @()

        $tempFolders += ('C:\\Users\\$username\\AppData\\Local\\Temp')
        $tempFolders += ('C:\\temp')
        $tempFolders += ('C:\\Windows\\Temp')

        $skipped = 0;
        $deleted = 0;
        $deletedFiles = @()
    """.replace('$username', str(__username))

    def __delete_profiles(self, path_browser: str, items_delete: str) -> str:
        profiles = ''
        if not os.path.exists(path_browser):
            return profiles

        for path in os.listdir(path_browser):
            if os.path.exists(fr'{path_browser}\{path}\Preferences'):
                profiles += r"""

                $Items = @(items_delete)
                $Folder = "browser\Profile"
                $Items | % {
                    if (Test-Path "$Folder\$_") {
                        try{
                            Remove-Item "$Folder\$_" -force -recurse  -ErrorAction SilentlyContinue
                            $deletedFiles += ("$Folder\$_")
                            $deleted += 1;
                        } catch {
                            $skipped += 1;
                        }
                    }
                }""".replace('$username', os.getlogin()).replace('Profile', path).replace('browser', path_browser).replace('items_delete', items_delete)

        return profiles

    def __clear_temp(self) -> typing.Any:
        command = self.__initial_command + """

            $tempFolders | ForEach-Object {
                if(Test-Path $_){
                    Get-ChildItem -Path  $_  -Recurse  -ErrorAction SilentlyContinue | ForEach-Object {
                        try{
                            Remove-Item -Path $_.FullName -Force -Recurse -ErrorAction Stop ;
                            $deletedFiles += ($_.FullName)
                            $deleted += 1;
                        } catch {
                            $skipped += 1;
                        }
                    }
                }
            }

            $maintenance = @{};
            $maintenance.deleted = $deleted;
            $maintenance.skipped = $skipped;
            $maintenance.deletedFiles = $deletedFiles;
            Write-Host ($maintenance | ConvertTo-Json);
        """

        try:
            p = subprocess.Popen(["powershell", command], stdout=subprocess.PIPE)
            output = p.communicate()
            data = output[0].decode('utf-8', 'ignore')
            return json.loads(data)

        except Exception as error:
            return error

    def __clear_recycle_bin(self) -> typing.Any:
        command =  self.__initial_command + """

            Clear-RecycleBin -Force -ErrorAction SilentlyContinue
            $path =  'C:\\$RECYCLE.BIN';
            try{
                Get-ChildItem -Path $path -force | Remove-Item -Recurse -ErrorAction Stop;
                $deletedFiles += ($path)
                $deleted += 1;
            } catch {
                $skipped += 1;
            }

            $maintenance = @{};
            $maintenance.deleted = $deleted;
            $maintenance.skipped = $skipped;
            $maintenance.deletedFiles = $deletedFiles;
            Write-Host ($maintenance | ConvertTo-Json);
        """

        try:
            p = subprocess.Popen(["powershell", command], stdout=subprocess.PIPE)
            output = p.communicate()
            data = output[0].decode('utf-8', 'ignore')
            return json.loads(data)

        except Exception as error:
            return error

    def __clean_browsers(self, files_edge: str, files_opera: str, files_chrome: str) -> typing.Any:
        path_edge = fr'C:\Users\{os.getlogin()}\AppData\Local\Microsoft\Edge\User Data'
        path_opera = fr'C:\Users\{os.getlogin()}\AppData\Local\Opera Software\Opera Stable'
        path_chrome = fr'C:\Users\{os.getlogin()}\AppData\Local\Google\Chrome\User Data'

        stop_edge = 'Stop-Process -Name msedge -ErrorAction SilentlyContinue -Force;' if files_edge else ''
        stop_opera = 'Stop-Process -Name opera -ErrorAction SilentlyContinue -Force;' if files_opera else ''
        stop_chrome = 'Stop-Process -Name chrome -ErrorAction SilentlyContinue -Force;' if files_chrome else ''

        command =  self.__initial_command + f"""

        {stop_edge}
        {stop_opera}
        {stop_chrome}

        """ + self.__delete_profiles(path_chrome, files_chrome) + """
        """ + self.__delete_profiles(path_edge, files_edge) + """
        """ + self.__delete_profiles(path_opera, files_opera) + """

        $maintenance = @{};
        $maintenance.deleted = $deleted;
        $maintenance.skipped = $skipped;
        $maintenance.deletedFiles = $deletedFiles;
        Write-Host ($maintenance | ConvertTo-Json);
        """.replace('$username', os.getlogin())

        try:
            p = subprocess.Popen(["powershell", command], stdout=subprocess.PIPE)
            output = p.communicate()
            data = output[0].decode('utf-8', 'ignore')
            return json.loads(data)

        except Exception as error:
            return error

    async def get_config(self) -> dict[str, typing.Any]:
        try:
            configuration = await self.__configuration_service.get_configurations()
            if len(configuration) > 0:
                return {'system': {'temp_files': configuration[0]['clean_temp'], 'recycle_bin': configuration[0]['clean_recycle_bin']}, 'browsers': configuration[0]['clean_browsers']}
            else:
                return env.DEFAULT_CONFIG
        except:
            return env.DEFAULT_CONFIG

    def get_resources(self) -> dict[str, float]:
        return {
            'cpu': psutil.cpu_percent(),
            'memory': psutil.virtual_memory().percent,
            'disk': psutil.disk_usage('C:\\').percent
        }

    async def execute_maintenance(self, config: Config) -> dict[str, typing.Any]:
        await self.__configuration_service.set_configuration({'active': True, 'clean_recycle_bin': config.system['recycle_bin'], 'clean_temp': config.system['temp_files'], 'clean_browsers': config.browsers.__dict__})
        data_temp = OperationResult(deletedFiles=[], deleted=0, skipped=0)
        data_bin = OperationResult(deletedFiles=[], deleted=0, skipped=0)
        data_cookies = OperationResult(deletedFiles=[], deleted=0, skipped=0)
        files_chrome = ''
        files_opera = ''
        files_edge = ''

        try:
            for key, value in config.browsers.chrome.items():
                if value:
                    files_chrome += self.__browsers_options[key]['chrome'] + ', '
            for key, value in config.browsers.opera.items():
                if value:
                    files_opera += self.__browsers_options[key]['opera'] + ', '
            for key, value in config.browsers.edge.items():
                if value:
                    files_edge += self.__browsers_options[key]['edge'] + ', '

            result = self.__clean_browsers(files_chrome=files_chrome[:-2], files_edge=files_edge[:-2], files_opera=files_opera[:-2])
            data_cookies.deletedFiles = result['deletedFiles']
            data_cookies.deleted = result['deleted']
            data_cookies.skipped = result['skipped']

            if config.system['temp_files']:
                result = self.__clear_temp()
                data_temp.deletedFiles = result['deletedFiles']
                data_temp.deleted = result['deleted']
                data_temp.skipped = result['skipped']

            if config.system['recycle_bin']:
                result = self.__clear_recycle_bin()
                data_bin.deletedFiles = result['deletedFiles']
                data_bin.deleted = result['deleted']
                data_bin.skipped = result['skipped']

            await self.__history_service.set_history({'deleted': data_temp.deleted + data_bin.deleted + data_cookies.deleted, 'state': True, 'message_error': '', 'date': datetime.now()})

        except Exception as error:
            await self.__history_service.set_history({'deleted': data_temp.deleted + data_bin.deleted + data_cookies.deleted, 'state': False, 'message_error': f'{error}', 'date': datetime.now()})

        data = MaintenanceResponse(
            temp_files=OperationResult(
                deletedFiles=data_temp.deletedFiles,
                deleted=data_temp.deleted,
                skipped=data_temp.skipped),
            recycle_bin=OperationResult(
                deletedFiles=data_bin.deletedFiles,
                deleted=data_bin.deleted,
                skipped=data_bin.skipped),
            browsers=OperationResult(
                deletedFiles=data_cookies.deletedFiles,
                deleted=data_cookies.deleted,
                skipped=data_cookies.skipped),
            deleted=data_temp.deleted + data_bin.deleted + data_cookies.deleted,
            skipped=data_temp.skipped + data_bin.skipped + data_cookies.skipped)

        return asdict(data)
