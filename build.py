import os
import venv
import subprocess


def main():
    print('***** Inicio *****')
    run_dir = os.path.abspath(__file__)
    run_dir = run_dir.replace('build.py', '')
    venv_dir = run_dir + 'venv'

    if not os.path.isdir(venv_dir):
        print('Creando entorno virtual...')
        builder = venv.EnvBuilder(system_site_packages=False, clear=True, symlinks=False, upgrade=False, with_pip=True)
        builder.create(venv_dir)

    print('Instalando pyinstaller en el entorno virtual...')
    pip_path = os.path.join(venv_dir, 'Scripts', 'pip')
    subprocess.run(f'{pip_path} install pyinstaller', shell=True, capture_output=True)

    print('Instalando paquetes de requirements.txt en el entorno virtual...')
    pip_path = os.path.join(venv_dir, 'Scripts', 'pip')
    subprocess.run(f'{pip_path} install -r requirements.txt', shell=True, capture_output=True)

    print('Obteniendo los nombres de los módulos instalados...')
    site_packages = os.path.join(venv_dir, 'Lib', 'site-packages')
    dirs = os.listdir(site_packages)
    module_list = list(filter(lambda x: os.path.isdir(f'{site_packages}\\{x}') and not x.startswith('_') and not x.endswith('info'), dirs))

    print('Creando el comando de compilación...')
    pyinstaller_path = os.path.join(venv_dir, 'Scripts', 'pyinstaller.exe')
    command = fr'{pyinstaller_path} --noconfirm --onefile --noconsole --add-data=minibuster.ico;minibuster.ico --add-data=lib;lib --add-data=static;static --add-data=templates;templates --runtime-tmpdir=^%LOCALAPPDATA^%\MiniBuster'
    for module in module_list:
        command = command + f' --hidden-import={module} --collect-submodules={module}'
    command = command + f' {run_dir}main.py'

    print('Compilando MiniBuster...')
    subprocess.run(command, shell=True)

    print('***** Finalizado *****')


if __name__ == '__main__':
    main()
