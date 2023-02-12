import subprocess

from lib import BaseService


class MaintenanceService(BaseService):
    def clear_temp(self):
        print('hola')
        options = {
            'clear_temps': True,
            'recycle_bin': False
        }
        power_shell_cmd = r''
        if options['clear_temps']:
            power_shell_cmd += r'''$objShell = New-Object -ComObject Shell.Application
            $objFolder = $objShell.Namespace(0xA)
            $WinTemp = "c:\Windows\Temp\*"
            #1# Remove Temp Files
            write-Host "Removing Temp" -ForegroundColor Green
            Set-Location “C:\Windows\Temp”
            Remove-Item * -Recurse -Force -ErrorAction SilentlyContinue
            Set-Location “C:\Windows\Prefetch”
            Remove-Item * -Recurse -Force -ErrorAction SilentlyContinue
            Set-Location “C:\Documents and Settings”
            Remove-Item “.\*\Local Settings\temp\*” -Recurse -Force -ErrorAction SilentlyContinue
            Set-Location “C:\Users”
            Remove-Item “.\*\Appdata\Local\Temp\*” -Recurse -Force -ErrorAction SilentlyContinue
            #2# Running Disk Clean up Tool

            Sleep 3
            write-Host "Cleanup task complete!" -ForegroundColor Yellow
            Sleep 3'''

        if options['recycle_bin']:
            power_shell_cmd = power_shell_cmd + r'  ' + r'''
            $Path = 'C' + ':\$Recycle.Bin'
            Get-ChildItem $Path -Force -Recurse -ErrorAction SilentlyContinue |
            Remove-Item -Recurse -exclude *.ini -ErrorAction SilentlyContinue
            write-Host "Recycle Bin is empty."'''


        print(power_shell_cmd)

        completed = subprocess.run(["powershell", "-Command", power_shell_cmd], capture_output=True)
        return completed

    async def delete_history_chrome(self):
        power_shell_cmd = r'''
            $UserName = (whoami).Split('\')[1]
            $UserName
            $Items = @("Cache", "Cache2\entries\", "ChromeDWriteFontCache", "Code Cache", "GPUCache", "JumpListIcons", "JumpListIconsOld", "JumpListIconsRecentClosed", "Media Cache", "History", "Service Worker", "Top Sites", "Visited Links", "Web Data")
            $Folder = "C:\Users\$UserName\AppData\Local\Google\Chrome\User Data\Default"
            $Items | % {
                if (Test-Path "$Folder\$_") {
                    Remove-Item "$Folder\$_" -Recurse
                }
            }
            Remove-Dir "C:\users\$user\AppData\Local\Google\Chrome\User Data\SwReporter\"
            '''

        completed = subprocess.run(["powershell", "-Command", power_shell_cmd], capture_output=True)
        return completed

