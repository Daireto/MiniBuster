import os
import typing
import psutil
import subprocess

from lib import BaseService

import env


class MaintenanceService(BaseService):

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

        $tempFolders += ('C:\\Users\\' + $username + '\\AppData\\Local\\Temp')
        $tempFolders += ('C:\\temp')
        $tempFolders += ('C:\\Windows\\Temp')

        $deleted = 0;
        $deletedFiles = @()
    """.replace('$username', str(__username))

    def __delete_profiles(self, path_browser: str, items_delete: str):
        profiles = ""
        for path in os.listdir(path_browser):
            if os.path.exists(fr'{path_browser}\{path}\Preferences'):
                profiles += r"""

                $Items = @(items_delete)
                $Folder = "browser\Profile"
                $Items | % {
                    if (Test-Path "$Folder\$_") {
                        Remove-Item "$Folder\$_" -force -recurse  -ErrorAction SilentlyContinue
                        $deletedFiles += ("$Folder\$_")
                        $deleted += 1
                    }
                }""".replace('$username', os.getlogin()).replace('Profile', path).replace('browser', path_browser).replace('items_delete', items_delete)
        return profiles

    def __clear_temp(self) -> typing.Any:
        command = self.__initial_command + """

            $tempFolders | ForEach-Object {
                if(Test-Path $_){
                    Get-ChildItem -Path  $_  -Recurse  -ErrorAction SilentlyContinue | ForEach-Object {
                        try{
                            Remove-Item -Path $_.FullName -Force -Recurse -ErrorAction SilentlyContinue ;
                            $deletedFiles += ($_.FullName)
                            $deleted += 1;
                        }
                        catch [UnauthorizedAccessException]{
                            $skipped += 1 ;
                        }
                    }
                }
            }
        """
        try:
            p = subprocess.Popen(["powershell", command], stdout=subprocess.PIPE)
            output = p.communicate()
            data = output[0].decode('utf-8', 'ignore')

            print(data)
            return data
        except Exception as error:
            print(error)
            return error

    def __delete_cookies(self, files_edge, files_opera, files_chrome) -> typing.Any:
        path_edge = fr'C:\Users\{os.getlogin()}\AppData\Local\Microsoft\Edge\User Data'
        path_opera = fr'C:\Users\{os.getlogin()}\AppData\Local\Opera Software\Opera Stable'
        path_chrome = fr'C:\Users\{os.getlogin()}\AppData\Local\Google\Chrome\User Data'

        command =  self.__initial_command + """

        Stop-Process -Name msedge -ErrorAction SilentlyContinue -Force;
        Stop-Process -Name opera -ErrorAction SilentlyContinue -Force;
        Stop-Process -Name chrome -ErrorAction SilentlyContinue -Force;
        """ + self.__delete_profiles(path_chrome, files_chrome) + """
        """ + self.__delete_profiles(path_edge, files_edge) + """
        """ + self.__delete_profiles(path_opera, files_opera) + """
        $maintenance = @{};
        $maintenance.deleted = $deleted;
        $maintenance.deletedFiles = $deletedFiles;
        Write-Host ($maintenance | ConvertTo-Json);
        """.replace('$username', os.getlogin())
        try:
            p = subprocess.Popen(["powershell", command], stdout=subprocess.PIPE)
            output = p.communicate()
            data = output[0].decode('utf-8', 'ignore')

            print(data)
            return data
        except Exception as error:
            print(error)
            return error

    def __clear_recycle_bin(self) -> typing.Any:
        command =  self.__initial_command + """

            Clear-RecycleBin -Force -ErrorAction SilentlyContinue
            $DiskData | ForEach-Object {
                $path =  'C:\\$RECYCLE.BIN';
                Get-ChildItem -Path $path -force | Remove-Item -Recurse -ErrorAction SilentlyContinue;
                $deletedFiles += ($path)
        }
        """
        try:
            p = subprocess.Popen(["powershell", command], stdout=subprocess.PIPE)
            output = p.communicate()
            data = output[0].decode('utf-8', 'ignore')

            print(data)
            return data
        except Exception as error:
            print(error)
            return error

    def get_config(self) -> dict[str, object]:
        return env.DEFAULT_CONFIG

    def get_resources(self) -> dict[str, float]:
        return {
            'cpu': psutil.cpu_percent(),
            'memory': psutil.virtual_memory().percent,
            'disk': psutil.disk_usage('C:\\').percent
        }

    def execute_maintenance(self, config: dict[str, dict[str, bool]]):
        data = {}
        data_bin = {}
        data_temp = {}
        data_cookies = {}
        files_chrome = ''
        files_opera = ''
        files_edge = ''
        if config['system']['temp_files']:
            data_temp = self.__clear_temp()
        if config['system']['recycle_bin']:
            data_bin = self.__clear_recycle_bin()
        if config['browsers']:
            for key, value in config['browsers']['chrome'].__dict__.items():
                if value:
                    files_chrome += self.__browsers_options[key]['chrome'] + ', '
            for key, value in config['browsers']['opera'].__dict__.items():
                if value:
                    files_opera += self.__browsers_options[key]['opera'] + ', '
            for key, value in config['browsers']['edge'].__dict__.items():
                if value:
                    files_edge += self.__browsers_options[key]['edge'] + ', '
            data_cookies = self.__delete_cookies(files_chrome=files_chrome[:-2], files_edge=files_edge[:-2], files_opera=files_opera[:-2])
        data['deletedFiles'] = data_temp['deletedFiles'] + data_bin['deletedFiles'] + data_cookies['deletedFiles']
        data['deleted'] = data_temp['deleted'] + data_bin['deleted'] + data_cookies['deleted']
        return data
