import paho.mqtt.client as mqtt
import threading
import time
import psutil
import socket
import pyautogui
import subprocess
import os
import sys
from dotenv import load_dotenv                                                                # User .env file to load confidential data without uploading them to GitHub
#import pyuac                                                                                 # Test if the app is running as admin
import json                                                                                   # For JSON data parsing
import logo                                                                                   # Show custom logo
import streamTool                                                                             # Check if Environmental Variable exists
from user import get_logged_in_username                                                       # Gets the username of the currently logged-in user despite whether the script is run with elevated privileges.
from winFingerprint import get_short_fingerprint                                              # Gets the last 10 digits of the Unique SHA-256 Fingerprint for the OS+Hardware
from process_num import get_process_count                                                     # Process Checker
from icon_data import GOOD_ICON_BASE64, WARN_ICON_BASE64, ERROR_ICON_BASE64, create_icon      # Icons as Base64 Data
from windows_pathlib import WindowsPathlib as WinPath                                         # Use windows %path% in python
from win11toast import toast, toast_async                                                     # Windows 11 Toast Notifications
from sys import exit                                                                          # Exit the script

load_dotenv()                                                                                 # Load the variables from the .env file

########################################################################################################

logo.show_logo()

########################################################################################################


# Vars
HOSTNAME = socket.gethostname()                # PC hostname
MACHINE_ID = get_short_fingerprint()           # PC 10 digit unique hash
USERNAME = get_logged_in_username()            # Current logged-in user

IconPath      = WinPath(r"%public%\\Icons\\")  # Root Dir for storing Icons
GoodIconPath  = f"{IconPath}good.png"          # Good/Checkmark icon
WarnIconPath  = f"{IconPath}warn.png"          # Warning/Exclamation icon
ErrorIconPath = f"{IconPath}error.png"         # Error/X icon

self_exe = os.path.basename(sys.executable)    # Grab the current exe name

g_mainscript = False                           # By default not to run the kill script loop TODO: What?

PUBLISH_TIMEOUT = 4                            # Timout in seconds before publishing the latest information
SHUTDOWN_TIMEOUT = "60"                        # Shutdown Timeout in seconds when receiving the shutdown command

DEBUG = True                                   # Debug Mode

# Using .env to not leak confidential data :)
WS_SERVER   = os.getenv("WS_SERVER")           # Websocket Server Location
WS_PORT     = int(os.getenv("WS_PORT"))        # Websocket Port
WS_USERNAME = os.getenv("WS_USERNAME")         # Websocket Username Authentication
WS_PASSWORD = os.getenv("WS_PASSWORD")         # Websocket Password Authentication

########################################################################################################


# Check if streamos is installed by checking its path

if streamTool.check():

    # Get a temp warning icon
    TempWarnIconPath = WinPath(r"%temp%\warn.png")
    
    create_icon(TempWarnIconPath, WARN_ICON_BASE64)
    
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


########################################################################################################


# Make the Icon DIR if it does not exist already
os.makedirs(IconPath, exist_ok=True)

# Create icons from base64 data
create_icon(GoodIconPath, GOOD_ICON_BASE64)
create_icon(WarnIconPath, WARN_ICON_BASE64)
create_icon(ErrorIconPath, ERROR_ICON_BASE64)


########################################################################################################


# Check if the exe (not python) [the exe compiled with pyinstaller] is already running, and if so, exit 

if get_process_count(self_exe) > 2 and self_exe != "python.exe": # When compiled as an exe with PyInstaller there are 2 instances of it https://stackoverflow.com/a/34197172
    # print(get_process_count(self_exe))
    toast(
        f"{self_exe} is already running", 
        "The new instance will exit", 
        icon=WarnIconPath,
        audio='ms-winsoundevent:Notification.Reminder',
        button='Ok'
    )
    exit()


########################################################################################################

#StreamUnlock = 'os.system(""" "C:\Program Files\Windows STEAM Tools\PsExec.exe" /accepteula -u %USERDOMAIN%\Admin -p D1IT@D0e -i schtasks /run /tn STREAM\StreamUnlock """)'
#StreamLock = 'os.system(""" "C:\Program Files\Windows STEAM Tools\PsExec.exe" /accepteula -u %USERDOMAIN%\Admin -p D1IT@D0e -i schtasks /run /tn STREAM\StreamLock """)'

# if pyuac.isUserAdmin():
#     StreamUnlock = 'subprocess.run(["streamos", "unlock"], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)'
#     StreamLock = 'subprocess.run(["streamos", "lock"], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)'
#     toast(
#         "Running as Admin", 
#         "The app is currently running with admin privileges", 
#         icon=WarnIconPath,
#         audio='ms-winsoundevent:Notification.Reminder',
#         duration='short',
#         button='Ok'
#     )
# else:
#     StreamUnlock = r'subprocess.run(["C:\\Program Files\\Windows STEAM Tools\\PsExec.exe", "/accepteula", "-u", "%USERDOMAIN%\\Admin", "-p", "D1IT@D0e", "-i", "schtasks", "/run", "/tn", "STREAM\\StreamUnlock"], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)'
#     StreamLock = r'subprocess.run(["C:\\Program Files\\Windows STEAM Tools\\PsExec.exe", "/accepteula", "-u", "%USERDOMAIN%\\Admin", "-p", "D1IT@D0e", "-i", "schtasks", "/run", "/tn", "STREAM\\StreamLock"], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)'




########################################################################################################

# ESports Kill App Toll Class and code.
# Made with help from BlackBox AI :)
class AppBlocker:
    def __init__(self):
        self.app_status = {
            "enable": False,
            "Epic": False,
            "Steam": False,
            "Battle": False,
            "Riot": False
        }
        self.mainscript_enabled = False
        self.lock = threading.Lock()
        self.kill_thread = threading.Thread(target=self.kill_apps_loop, daemon=True)
        self.kill_thread.start()

    def update_status(self, data):
        with self.lock:
            self.mainscript_enabled   = data.get("enable", False)
            self.app_status["Epic"]   = data.get("Epic",   False)
            self.app_status["Steam"]  = data.get("Steam",  False)
            self.app_status["Battle"] = data.get("Battle", False)
            self.app_status["Riot"]   = data.get("Riot",   False)

    def kill_apps_loop(self):
        while True:
            time.sleep(4)  # Check every 4 seconds
            with self.lock:
                if self.mainscript_enabled:
                    self.check_and_kill_apps()

    def check_and_kill_apps(self):
        for app, should_kill in self.app_status.items():
            if should_kill:
                print(f"KS: Killing {app}")
                self.kill_app(app)

    def kill_app(self, app_name):
        app_map = {
            "Epic": ["EpicGamesLauncher.exe", "EpicWebHelper.exe"],
            "Steam": ["steam.exe"],
            "Battle": ["battle.net.exe"],
            "Riot": ["RiotClientUx.exe", "RiotClientServices.exe"]
        }

        def kill_process_and_children(proc):
            # Get the children of the current process
            children = proc.children(recursive=True)  # Get all child processes
            for child in children:
                try:
                    child.kill()  # Kill each child process
                    print(f"Killed child process: {child.name()} (PID: {child.pid})")
                except Exception as e:
                    print(f"Error killing child process {child.name()}: {e}")

            # Now kill the parent process
            try:
                proc.kill()
                print(f"Killed process: {proc.name()} (PID: {proc.pid})")
            except Exception as e:
                print(f"Error killing process {proc.name()}: {e}")

        for process in app_map.get(app_name, []):
            for proc in psutil.process_iter(attrs=['pid', 'name']):
                if proc.info['name'] == process:
                    kill_process_and_children(proc)



########################################################################################################


def shutdown_pc():
    #shutdown /s /t 60 /c "I'm tired, shutting down in 10 seconds"
    subprocess.run(
        ["shutdown", "/s", "/t", SHUTDOWN_TIMEOUT, "/c", f"I'm tired, shutting down in {SHUTDOWN_TIMEOUT} seconds"],
        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
    )

def show_test_notification():
    toast(
        "Test",
        "Test Succesfull",
        icon=GoodIconPath,
        audio='ms-winsoundevent:Notification.SMS',
        button='Nice :)'
    )

# Run Minecraft Education Edition
def run_MCEdu():
    print("\nLaunching MCEdu\n")
    # exec("os.system('start minecraftedu://')")
    subprocess.run(
        ["start", "minecraftedu://"],
        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
    )


# Function to publish messages in a loop
def publish_loop():
    while True:
        # CPU Usage Percentage
        cpu_percent = psutil.cpu_percent()
        client.publish(f"PC/{MACHINE_ID}/cpu", cpu_percent)

        # Ram Percentage
        ram_percent = str(psutil.virtual_memory().percent)
        client.publish(f"PC/{MACHINE_ID}/ram", ram_percent)

        # Current Focused App
        window_title = pyautogui.getActiveWindowTitle()
        client.publish(f"PC/{MACHINE_ID}/app", window_title)

        # Current User
        client.publish(f"PC/{MACHINE_ID}/user", USERNAME)

        # Current Hostname
        client.publish(f"PC/{MACHINE_ID}/hostname", HOSTNAME)

        # Print the data if debugging
        if DEBUG: print(f"Data Sent: \n  CPU: {cpu_percent}% \n  Ram: {ram_percent}%\n  App: {window_title}\n  User: {USERNAME}\n\n----------------------\n")

        time.sleep(PUBLISH_TIMEOUT)

########################################################################################################


def on_connect(client, userdata, flags, reason_code, properties):
    # Subscribe to a topic to listen for specific messages
    client.subscribe("ESports/status")
    client.subscribe(f"PC/{MACHINE_ID}/action")

    def main():
        toast(
            "Yippee",
            "Connected to Server",
            icon=GoodIconPath,
            audio='ms-winsoundevent:Notification.SMS'
        )
    threading.Thread(target=main).start()
    # Threads exits once the function is done
    print("Connected")


# The callback for when the client receives a message
def on_message(client, userdata, message):
    # Action data on what to do
    # Using predefined variables
    if message.topic == f"PC/{MACHINE_ID}/action":
        print(f"\nAction: {message.payload.decode()}\n")
        action = message.payload.decode()

        if action == "test":
            show_test_notification()
        if action == "none":
            print("\nNo Action to Do\n")
        if action == "shutdown":
            shutdown_pc()
        if action == "MCEdu":
            run_MCEdu()

        # if action == "lock":
        #     print("\nLocking the system\n")
        #     exec(StreamLock)
        # if action == "unlock": 
        #     print("\nUnlocking the system\n")
        #     exec(StreamUnlock)

    

    if message.topic == "ESports/status":
        print("Status Received")
        status_json = message.payload.decode()
        try:
            data = json.loads(status_json)
            app_blocker.update_status(data)
        except json.JSONDecodeError:
            print("Failed to decode JSON")
    






# Initialize the AppBlocker
app_blocker = AppBlocker()

# Connect to the MQTT broker
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, transport="websockets")
client.username_pw_set(username=WS_USERNAME, password=WS_PASSWORD)
client.on_message = on_message
client.on_connect = on_connect

try:
    client.connect(WS_SERVER, WS_PORT)
except: 
    toast(
        "Uh Oh", 
        "Unable to connect to the Server for Data\nPlease check your internet connection", 
        icon=ErrorIconPath,
        audio='ms-winsoundevent:Notification.Reminder',
        duration='short'
    )
    exit()

# Start the MQTT client loop in a separate thread
client.loop_start()

# Set the current action to none
# client.publish(f"PC/{MACHINE_ID}/action", "none", 0, True)
client.publish(f"PC/{MACHINE_ID}/action", "none")

# Start the publishing loop in another thread
publish_thread = threading.Thread(target=publish_loop)
publish_thread.start()


# # Start the Kill ESports thread
# kill_esports_thread = threading.Thread(target=kill_esports_loop)
# kill_esports_thread.start()



publish_thread.join()
# kill_esports_thread.join()