import os
from qgis.core import QgsSettings

# D:\QGIS>pip install cryptography
# D:\QGIS>pip install web3
# D:\QGIS>pip install python-dotenv
# D:\QGIS>pip install xkcdpass
# D:\QGIS>pip install easygui or python -m pip install easygui
# D:\QGIS>pip install python-dotenv
# D:\QGIS>(python -m) pip install pyqt-switch

def apply_settings():

    # Create a QgsSettings object
    settings = QgsSettings()

    # Check if the plugin has been run before
    if not settings.value("MapSafe/first_run", defaultValue=True, type=bool):
        # This is not the first run, so just return
        print('Not first run')
        return

    package = "cryptography"
    try:
        import cryptography
    except:
        print(f"--------------- INSTALLING {package} --------------------------------")
        os.system("pip install -U "+ package)
        print('Installing package ' + package)

    package = "python-dotenv"
    try:
        from dotenv import load_dotenv
    except:
        print(f"--------------- INSTALLING {package} --------------------------------")

        os.system("pip install -U "+ package)
        print('Installing package ' + package)

    from dotenv import load_dotenv
    load_dotenv()


    package = "envs"
    try:
        import envs as env
    except:
        print(f"--------------- INSTALLING {package} --------------------------------")
        os.system("pip install "+ package)
        print('Installing package ' + package)


    # package = "pathlib"
    # try:
    #     import pathlib
    # except:
    #     print(f"--------------- INSTALANDO {package} --------------------------------")
    #     os.system("pip install "+ package)


    package = "pyqt-switch"
    try:
        jw = __import__('pyqt-switch')
    except:
        print(f"--------------- INSTALLING {package} --------------------------------")
        os.system("pip install -U "+ package)
        print('Installing package ' + package)

    package = "easygui"
    try:
        import easygui
    except:
        print(f"--------------- INSTALLING {package} --------------------------------")
        os.system("pip install -U "+ package)
        print('Installing package ' + package)

    package = "xkcdpass"
    try:
        import xkcdpass
    except:
        print(f"--------------- INSTALLING {package} --------------------------------")
        os.system("pip install -U "+ package)
        print('Installing package ' + package)

    package = "web3"
    try:
        import web3
    except:
        print(f"--------------- INSTALLING {package} --------------------------------")
        os.system("pip install -U "+ package)
        print('Installing package ' + package)

    # After applying first-run settings, set the flag to False
    settings.setValue("MapSafe/first_run", False)
    print('Set first run = false')