from icon_data import WARN_ICON_BASE64, create_icon     # Icons as Base64 Data
from windows_pathlib import WindowsPathlib as WinPath   # Use windows %path% in python
from win11toast import toast                            # Windows 11 Toast Notifications
from logo import CENTER_TEXT_WIDTH                      # Get the console width to center text varaible
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

def bool_check():
    """
    The main boolean function that checks whether the STREAMOS tool is present or if there is a bypass to allow the script in app.py to continue.
    :return: Boolean for the script in app.py to continue or not
    """
    if not exist() and not bypass():
        return True
    else:
        return False


def check():
    if bool_check():
        # Get a temp warning icon
        TempWarnIconPath = WinPath(r"%temp%\warn.png")
        create_icon(TempWarnIconPath, WARN_ICON_BASE64)

        print("")
        print("ERROR: streamos command line tool is not installed".center(CENTER_TEXT_WIDTH))
        print("Please install STREAM-OS properly before using this app".center(CENTER_TEXT_WIDTH))
        print("")

        toast(
            "STREAM-OS not installed",
            "This app will not work if STREAM-OS is not installed\nPlease install STREAM-OS properly before using this app",
            icon=fr"{TempWarnIconPath}",
            audio='ms-winsoundevent:Notification.Reminder',
            duration='long',
            button='Ok'
        )
        os.remove(TempWarnIconPath)

        exit()



if __name__ == "__main__":
    if bypass():
        print("Bypassed")
    else:
        print("Not Bypassed")

    if not exist():
        print("Not Installed")
    else:
        print("Installed")

    if bool_check():
        # True - Show Message
        print("Does not exist and not bypassed")
    else:
        # False - Do not show message and continue on
        print("exists or bypassed")