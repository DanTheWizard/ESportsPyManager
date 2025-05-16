from windows_pathlib import WindowsPathlib as WinPath
import os

def bypass():
    """
    Checks whether there is a file in the public directory to bypass this check.
    Useful only for debugging and/or non-streamos tasks
    :return: Boolean whether it exists or not
    """
    if os.path.exists(WinPath(r"%public%\.NoStreamOS")):
        return True
    else:
        return False
    
def exist():
    """
    Checks whether the STREAMOS tool is present or not.
    .bat and .cmd for compatibility until .exe is finished
    :return: Boolean whether it exists or not
    """
    if os.path.exists(WinPath(r"%programfiles%\STREAMOS\streamos.bat")) or os.path.exists(WinPath(r"%programfiles%\STREAMOS\streamos.exe")) or os.path.exists(WinPath(r"%programfiles%\STREAMOS\streamos.cmd")):
        return True
    else:
        return False

def check():
    """
    The main function that checks whether the STREAMOS tool is present or if there is a bypass to allow the script in app.py to continue.
    :return: Boolean for the script in app.py to continue or not
    """
    if not exist() and not bypass():
        return True
    else:
        return False




if __name__ == "__main__":
    if bypass():
        print("Bypassed")
    else:
        print("Not Bypassed")

    if not exist():
        print("Not Installed")
    else:
        print("Installed")

    if check():
        # True - Show Message
        print("Does not exist and not bypassed")
    else:
        # False - Do not show message and continue on
        print("exists or bypassed")