import os
import typing
import psutil
import subprocess

from lib import BaseService

import env


class MaintenanceService(BaseService):

    __initial_command = """
        $items = 0;
        $disco = 'C';
        $DiskData = @() ;
        get-wmiobject Win32_LogicalDisk | ? { $_.drivetype -eq 3 } | % { get-psdrive $_.deviceid[0] } | ForEach-Object {
            $disk = @{};
            $disk.Nombre = $_.Name;
            $disk.Uso = [math]::Round(($_.Used / 1gb), 2);
            $disk.Libre = [math]::Round(($_.Free / 1gb), 2);
            $disk.Raiz = $_.Root;
            $DiskData += $disk;
        }
        #$folders = @()
        $tempFolders = @()
        $username = (Get-WmiObject -ComputerName $env:COMPUTERNAME -Class Win32_ComputerSystem | Select-Object UserName).Username;
        if($username.Length -gt 0){
            if($username.split('\\').Length -gt 1){
                $username = $username.split('\\')[1]
            }
        }else{
            $queryResults = (qwinsta /server:localhost)
            if((GET-WinSystemLocale).Name.Substring(0,2) -eq "es"){
                $values = ($queryResults -Match 'Activo')
            }else{
                $values =  ($queryResults -Match 'Active')
            }
            for($i = 0; $i -lt 10; $i++){
                $values = $values-replace "  ", " "
            }
            $values.split(" ")[2]
            $username = $values.split(" ")[2]
        }

        $DiskData | ForEach-Object {
            $tempFolders += ($_.Nombre + ':\\Users\\' + $username + '\\AppData\\Local\\Temp')
            $tempFolders += ($_.Nombre + ':\\temp')
            $tempFolders += ($_.Nombre + ':\\Windows\\Temp')
        }

        $deleted = 0;
        $deletedFolders = @()
        $deletedFiles = @()
        $skipped = 0;
    """

    def get_config(self) -> dict[str, object]:
        return env.DEFAULT_CONFIG

    def get_resources(self) -> dict[str, float]:
        return {
            'cpu': psutil.cpu_percent(),
            'memory': psutil.virtual_memory().percent,
            'disk': psutil.disk_usage(os.getcwd()).percent
        }

    def clear_temp(self) -> typing.Any:
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

    def delete_cookies(self) -> typing.Any:
        command =  self.__initial_command + r"""

            Stop-Process -Name msedge -ErrorAction SilentlyContinue -Force;
            Stop-Process -Name opera -ErrorAction SilentlyContinue -Force;
            Stop-Process -Name chrome -ErrorAction SilentlyContinue -Force;
            $DaysToDelete = 0

            $DiskData | ForEach-Object {
                $ItemsGoogle = @("Cache", "Cache2\entries\", "ChromeDWriteFontCache", "Code Cache", "GPUCache", "JumpListIcons", "JumpListIconsOld", "JumpListIconsRecentClosed", "Media Cache", "History", "Service Worker", "Top Sites", "Visited Links", "Web Data", "Login Data", "Cookies")
                $Folder = "C:\Users\" + $username + \AppData\Local\Google\Chrome\User Data\Default"
                $ItemsGoogle | % {
                    if (Test-Path "$Folder\$_") {
                        Remove-Item "$Folder\$_" -force -recurse  -ErrorAction SilentlyContinue
                        $deletedFiles += ($_.FullName)
                    }
                }

                $ItemsEdge = @("Cache", "Cache2\entries\", "ChromeDWriteFontCache", "Code Cache", "GPUCache", "JumpListIcons", "JumpListIconsOld", "JumpListIconsRecentClosed", "Media Cache", "History", "Service Worker", "Top Sites", "Visited Links", "Web Data", "Cookies")
                $Folder = "C:\Users\" + $username + \AppData\Local\Microsoft\Edge\User Data\Default"
                $ItemsEdge | % {
                    if (Test-Path "$Folder\$_") {
                        Remove-Item "$Folder\$_" -force -recurse  -ErrorAction SilentlyContinue
                        $deletedFiles += ($_.FullName)
                    }
                }

                $ItemsOpera = @("Cache", "Cache2\entries\", "ChromeDWriteFontCache", "Code Cache", "GPUCache", "JumpListIcons", "JumpListIconsOld", "JumpListIconsRecentClosed", "Media Cache", "History", "Service Worker", "Top Sites", "Visited Links", "Web Data", "Cookies")
                $Folder = "C:\Users\" + $username + \AppData\Local\Opera Software\Opera Stable")
                $ItemsOpera | % {
                    if (Test-Path "$Folder\$_") {
                        Remove-Item "$Folder\$_" -force -recurse  -ErrorAction SilentlyContinue
                        $deletedFiles += ($_.FullName)
                    }
                }
            }

            $maintenance = @{};
            $maintenance.deleted = $deleted;
            $maintenance.deletedFiles = $deletedFiles;
            Write-Host ($maintenance | ConvertTo-Json);
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

    def clear_recycle_bin(self) -> typing.Any:
        command =  self.__initial_command + """

            Clear-RecycleBin -Force -ErrorAction SilentlyContinue
            $DiskData | ForEach-Object {
                $path =  $_.Nombre + ':\\$RECYCLE.BIN';
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

    def execute_maintenance(self, config: dict[str, object]):
        data_bin = self.clear_recycle_bin();
        data_temp = self.clear_temp();
        data_cookies = self.delete_cookies();
        return 'Hello, World!'

