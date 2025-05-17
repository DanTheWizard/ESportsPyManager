from user import get_logged_in_username                 # Gets the username of the currently logged-in user despite whether the script is run with elevated privileges.
from winFingerprint import get_short_fingerprint        # Gets the last 10 digits of the Unique SHA-256 Fingerprint for the OS+Hardware
from dotenv import load_dotenv                          # User .env file to load confidential data without uploading them to GitHub
from windows_pathlib import WindowsPathlib as WinPath   # Use windows %path% in python
import socket
import sys
import os


"""
All the main variables for app.py
"""

load_dotenv()                                  # Load the variables from the .env file

IconPath      = WinPath(r"%public%\\Icons\\")  # Root Dir for storing Icons
GoodIconPath  = f"{IconPath}good.png"          # Good/Checkmark icon
WarnIconPath  = f"{IconPath}warn.png"          # Warning/Exclamation icon
ErrorIconPath = f"{IconPath}error.png"         # Error/X icon

self_exe = os.path.basename(sys.executable)    # Grab the current exe name


PUBLISH_TIMEOUT           = 4                  # Timout in seconds before publishing the latest information
DEFAULT_SHUTDOWN_TIMEOUT  = 60                 # Shutdown Timeout in seconds when receiving the shutdown command
KILL_LOOP_TIMEOUT         = 4                  # Timeout in seconds before running the kill loop


SHOW_WS_URL_PORT_STARTUP = False               # Show the WebSocket url:port on the main startup after connecting successfully


# Debugging
DEBUG           = True                         # Debug Mode
DEBUG_PUBLISH   = False                        # Enable Print out of the Publishing Data to the WebSocket Server
DEBUG_KILL      = False                        # Enable Print out of the Simple killing app
DEBUG_KILL_ADV  = False                        # Enable Print out of the Simple killing app


# Machine Information
HOSTNAME = socket.gethostname()                # PC hostname
MACHINE_ID = get_short_fingerprint()           # PC 10 digit unique hash
USERNAME = get_logged_in_username()            # Current logged-in user


# WebSocket connection details
# Using .env to not leak confidential data :)
WS_SERVER   = os.getenv("WS_SERVER")           # Websocket Server Location
WS_PORT     = int(os.getenv("WS_PORT"))        # Websocket Port
WS_USERNAME = os.getenv("WS_USERNAME")         # Websocket Username Authentication
WS_PASSWORD = os.getenv("WS_PASSWORD")         # Websocket Password Authentication
