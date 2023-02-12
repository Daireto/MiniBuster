import psutil
import subprocess

from lib import BaseService


class MaintenanceService(BaseService):
    
    def hello_world(self):
        memory =  psutil.virtual_memory()[2]
        return f"Hello, World! ${memory}"

    async def clear_temp(self):
        power_shell_cmd = r'''$objShell = New-Object -ComObject Shell.Application 
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
        write-Host "Running the Windows Disk Clean up Tool" -ForegroundColor White  
        cleanmgr /sagerun:1 | out-Null  
        $([char]7)  
        Sleep 3  
        write-Host "Cleanup task complete!" -ForegroundColor Yellow  
        Sleep 3'''

        completed = subprocess.run(["powershell", "-Command", power_shell_cmd], capture_output=True)
        return completed
    
    async def delete_history_chroome(self):
        power_shell_cmd = r'''            
            $UserName = (whoami).Split('\')[1]
            $UserName  
            $Items = @('Archived History', 
                        'History',  
                        'Cache', 
                        'Visited Links') 
            $Folder = "C:\Users\$UserName\AppData\Local\Google\Chrome\User Data\Default" 
            $Items | % {  
                if (Test-Path "$Folder\$_") { 
                    Remove-Item "$Folder\$_"  
                } 
            } '''

        completed = subprocess.run(["powershell", "-Command", power_shell_cmd], capture_output=True)
        return completed

