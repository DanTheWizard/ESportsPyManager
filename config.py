from user import get_logged_in_username                 # Gets the username of the currently logged-in user despite whether the script is run with elevated privileges.
from winFingerprint import get_short_fingerprint        # Gets the last 10 digits of the Unique SHA-256 Fingerprint for the OS+Hardware
from dotenv import load_dotenv                          # User .env file to load confidential data without uploading them to GitHub
from windows_pathlib import WindowsPathlib as WinPath   # Use windows %path% in python
import socket
import sys
import os


"""
All the main variables for app.py to operate
"""


load_dotenv()                                  # Load the variables from the .env file


IconPath      = WinPath(r"%public%\\Icons\\")  # Root Dir for storing Icons
WarnIconPath  = f"{IconPath}warn.png"          # Warning/Exclamation icon
GoodIconPath  = f"{IconPath}good.png"          # Good/Checkmark icon
ErrorIconPath = f"{IconPath}error.png"         # Error/X icon


self_exe = os.path.basename(sys.executable)    # Grab the current exe name


# Timeout settings
PUBLISH_TIMEOUT           = 4                  # Timout in seconds before publishing PC data
KILL_LOOP_TIMEOUT         = 4                  # Timeout in seconds before running the kill loop
DEFAULT_SHUTDOWN_TIMEOUT  = 60                 # Shutdown Timeout in seconds when receiving the shutdown command


SHOW_WS_URL_PORT_STARTUP = False               # Show the WebSocket url:port on the main startup after connecting successfully


# Debugging (I do not recommend enabling all of them at once)
DEBUG           = False                        # Debug Mode (simple lines)
DEBUG_PUBLISH   = False                        # Enable Print out of the Publishing Data to the WebSocket Server
DEBUG_STATUS    = False                        # Enable Print out of the Receiving Status
DEBUG_KILL      = False                        # Enable Print out of the Simple killing app
DEBUG_KILL_ADV  = False                        # Enable Print out of the advanced killing information
DEBUG_WS_MES    = False                        # Enable Print out of some extra details when receiving data from WS Server (Adv)
DEBUG_WS_CON    = False                        # Enable Print out of some extra connection details when connecting to the WS server (Adv)


# Machine Information
HOSTNAME   = socket.gethostname()              # PC hostname
MACHINE_ID = get_short_fingerprint()           # PC 10 digit unique hash
USERNAME   = get_logged_in_username()          # Current logged-in user


# WebSocket connection details
# Using .env to not leak confidential data :)
WS_SERVER   = os.getenv("WS_SERVER")           # Websocket Server Location
WS_PORT     = int(os.getenv("WS_PORT"))        # Websocket Port
WS_USERNAME = os.getenv("WS_USERNAME")         # Websocket Username Authentication
WS_PASSWORD = os.getenv("WS_PASSWORD")         # Websocket Password Authentication



if __name__ == "__main__":
    print("----------------------------------------------------------")
    print("IconPath:     ", IconPath)
    print("WarnIconPath: ", WarnIconPath)
    print("GoodIconPath: ", GoodIconPath)
    print("ErrorIconPath:", ErrorIconPath)
    print("----------------------------------------------------------")
    print("self_exe:", self_exe)
    print("----------------------------------------------------------")
    print("PUBLISH_TIMEOUT:         ", PUBLISH_TIMEOUT)
    print("KILL_LOOP_TIMEOUT:       ", KILL_LOOP_TIMEOUT)
    print("DEFAULT_SHUTDOWN_TIMEOUT:", DEFAULT_SHUTDOWN_TIMEOUT)
    print("----------------------------------------------------------")
    print("SHOW_WS_URL_PORT_STARTUP:", SHOW_WS_URL_PORT_STARTUP)
    print("----------------------------------------------------------")
    print("DEBUG0         ", DEBUG)
    print("DEBUG_PUBLISH: ", DEBUG_PUBLISH)
    print("DEBUG_STATUS:  ", DEBUG_STATUS)
    print("DEBUG_KILL:    ", DEBUG_KILL)
    print("DEBUG_KILL_ADV:", DEBUG_KILL_ADV)
    print("DEBUG_WS_MES:  ", DEBUG_WS_MES)
    print("DEBUG_WS_CON:  ", DEBUG_WS_CON)
    print("----------------------------------------------------------")
    print("HOSTNAME:  ", HOSTNAME)
    print("MACHINE_ID:", MACHINE_ID)
    print("USERNAME:  ", USERNAME)
    print("----------------------------------------------------------")
    print("WS_SERVER:  ", WS_SERVER)
    print("WS_PORT:    ", WS_PORT)
    print("WS_USERNAME:", WS_USERNAME)
    print("WS_PASSWORD:", WS_PASSWORD)
    print("----------------------------------------------------------")
