from winFingerprint import get_short_fingerprint        # Gets the last 10 digits of the Unique SHA-256 Fingerprint for the OS+Hardware
from dotenv import load_dotenv                          # User .env file to load confidential data without uploading them to GitHub
from windows_pathlib import WindowsPathlib as WinPath   # Use windows %path% in python
from override import get_override                       # Use variables in override.ini over the default (Useful for debugging)
from envpath import dotenv_path                         # Dynamic exe .env path location (I need to find a better way to secure this to prevent values from .env to be easily readable)
import actions                                          # Set of actions to do based on received WebSocket action string
import socket
import sys
import os


"""
All the main variables for app.py to operate
Most can be overridden with override.ini for debugging
"""


load_dotenv(dotenv_path)                                 # Load the variables from the .env file



APPS_LIST = {
    "Epic":   False,
    "Steam":  False,
    "Battle": False,
    "Riot":   False,
    "MCJava": False,
    "MCEdu":  False
} ; "List of all the apps to kill, with a default value of whether to kill or not (False = do not kill, True = kill)"


APP_MAP = {
    "Epic":   ["EpicGamesLauncher.exe", "EpicWebHelper.exe"],
    "Steam":  ["steam.exe"],
    "Battle": ["battle.net.exe"],
    "Riot":   ["RiotClientUx.exe", "RiotClientServices.exe"],
    "MCJava": ["javaw.exe", "MinecraftLauncher.exe"],
    "MCEdu":  ["Minecraft.Windows.exe"]
} ; "Map of all the apps to kill, with the first item being the main app from APP_LIST and the rest being the exe names"

ACTION_MAP = {
    "none":     lambda _: actions.none_action(),
    "test":     lambda _: actions.show_test_notification(),
    "MCEdu":    lambda _: actions.run_MCEdu(),
    "MCJava":   lambda _: actions.run_MCJava(),
    "ID":       lambda _: actions.messageboxMachineID(),
    "reboot":   lambda _: actions.reboot_pc(),
    "shutdown": lambda arg_timeout: actions.shutdown_pc(arg_timeout or DEFAULT_SHUTDOWN_TIMEOUT),
    "say":      lambda arg_words:   actions.say(arg_words),
    # "lock": lambda _: exec(StreamLock),
    # "unlock": lambda _: exec(StreamUnlock),
}


IconPath                  = WinPath(r"%public%\\Icons\\")       ;"Root Dir location for storing Icons"
WarnIconPath              = f"{IconPath}warn.png"               ;"Warning/Exclamation icon path"
GoodIconPath              = f"{IconPath}good.png"               ;"Good/Checkmark icon path"
ErrorIconPath             = f"{IconPath}error.png"              ;"Error/X icon path"

self_exe                  = os.path.basename(sys.executable)    ;"Grab the current focused exe title as string"


# Machine Information
HOSTNAME                  = socket.gethostname()                ;"PC hostname"
MACHINE_ID                = get_short_fingerprint()             ;"PC 10 digit unique hash"


# Timeout settings
PUBLISH_TIMEOUT           = get_override("PUBLISH_TIMEOUT",          4,  int)        ;"Timout in seconds before publishing PC data | Default: 4"
KILL_LOOP_TIMEOUT         = get_override("KILL_LOOP_TIMEOUT",        4,  int)        ;"Timeout in seconds before running the kill loop | Default: 4"
DEFAULT_SHUTDOWN_TIMEOUT  = get_override("DEFAULT_SHUTDOWN_TIMEOUT", 60, int)        ;"Shutdown Timeout in seconds when receiving the shutdown command | Default: 60"


# Debugging (I do not recommend enabling all of them at once)
DEBUG                     = get_override("DEBUG",          False, bool)              ;"Debug Mode (simple lines) | Default: False"
DEBUG_PUBLISH             = get_override("DEBUG_PUBLISH",  False, bool)              ;"Enable Print out of the Publishing Data to the WebSocket Server | Default: False"
DEBUG_STATUS              = get_override("DEBUG_STATUS",   False, bool)              ;"Enable Print out of the Receiving Status | Default: False"
DEBUG_KILL                = get_override("DEBUG_KILL",     False, bool)              ;"Enable Print out of the Simple killing app | Default: False"
DEBUG_KILL_ADV            = get_override("DEBUG_KILL_ADV", False, bool)              ;"Enable Print out of the advanced killing information | Default: False"
DEBUG_WS_MES              = get_override("DEBUG_WS_MES",   False, bool)              ;"Enable Print out of some extra details when receiving data from WS Server (Adv) | Default: False"
DEBUG_WS_CON              = get_override("DEBUG_WS_CON",   False, bool)              ;"Enable Print out of some extra connection details when connecting to the WS server (Adv) | Default: False"


# WebSocket connection details
# Using .env to not leak confidential data :)
WS_SERVER                 = os.getenv("WS_SERVER")           ;"Websocket Server Location"
WS_PORT                   = int(os.getenv("WS_PORT"))        ;"Websocket Port"
WS_USERNAME               = os.getenv("WS_USERNAME")         ;"Websocket Username Authentication"
WS_PASSWORD               = os.getenv("WS_PASSWORD")         ;"Websocket Password Authentication"

WS_USE_TLS                = get_override("WS_USE_TLS",               True,  bool)    ;"Whether to use TLS (SSL) connection when connecting to the WebSocket Server | Default: True"
WS_SHOW_CON_TOAST         = get_override("WS_SHOW_CON_TOAST",        False, bool)    ;"Show a notification that Connecting to server was a success | Default: False"
SHOW_WS_URL_PORT_STARTUP  = get_override("SHOW_WS_URL_PORT_STARTUP", False, bool)    ;"Show the WebSocket url:port on the main startup after connecting successfully | Default: False"


if __name__ == "__main__":
    # Override.ini must be placed in the src folder to run this test (only for this config.py __name__ = "__main__")
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
    print("----------------------------------------------------------")
    print("WS_SERVER:  ", WS_SERVER)
    print("WS_PORT:    ", WS_PORT)
    print("WS_USERNAME:", WS_USERNAME)
    print("WS_PASSWORD:", WS_PASSWORD)
    print("----------------------------------------------------------")
