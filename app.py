import paho.mqtt.client as mqtt                                                               # The WebSocket (and MQTT) library for connecting to a WS server
import threading                                                                              # Used to run multiple functions at once
import psutil                                                                                 # Used to kill processes (using subprocess taskkill led to antivirus triggers)
import json                                                                                   # For JSON data parsing
import time                                                                                   # Well... to set timeouts
import actions                                                                                # Set of actions to do based on received WebSocket action string
import streamTool                                                                             # Check if Environmental Variable exists
from logo import *                                                                            # Show custom logo and Main width for text if to be centered
from debugPrint import *                                                                      # Import the Debug Print Functions
from datetime import datetime                                                                 # Used to get current time for server detection when a device was last online
from process_num import get_process_count                                                     # Process Checker
from icon_data import GOOD_ICON_BASE64, WARN_ICON_BASE64, ERROR_ICON_BASE64, create_icon      # Icons as Base64 Data
from pyautogui import getActiveWindowTitle                                                    # Get the current focused app name
from win11toast import toast                                                                  # Windows 11 Toast Notifications
from sys import exit                                                                          # Exit the script
from config import *                                                                          # Import all variables and imports from config (cleaner structure)

########################################################################################################

show_logo()

########################################################################################################

# Check if STREAMOS tool is installed by checking its path
streamTool.check()

########################################################################################################

# Make the Icon DIR if it does not exist already
os.makedirs(IconPath, exist_ok=True)

# Create icons from base64 data
create_icon(GoodIconPath, GOOD_ICON_BASE64)
create_icon(WarnIconPath, WARN_ICON_BASE64)
create_icon(ErrorIconPath, ERROR_ICON_BASE64)

########################################################################################################


# Check if the exe (not python) [the exe compiled with pyinstaller] is already running, and if so, exit 

if get_process_count(self_exe) > 2 and self_exe != "python.exe": # When compiled as an exe with PyInstaller, there are 2 instances of it https://stackoverflow.com/a/34197172
    # print(get_process_count(self_exe))
    print("")
    print(f"ERROR: {self_exe} is already running".center(CENTER_TEXT_WIDTH))
    print("This new instance will exit".center(CENTER_TEXT_WIDTH))
    print("")
    toast(
        f"{self_exe} is already running", 
        "This new instance will exit",
        icon=WarnIconPath,
        audio='ms-winsoundevent:Notification.Reminder',
        button='Ok'
    )
    exit()


########################################################################################################


# ESports Kill App Toll Class and code.
# Made with help from ChatGPT :)
def kill_app(app_name):
    """
    Finds and kills a given application and its child processes based on predefined executable names.
    """
    app_map = {
        "Epic": ["EpicGamesLauncher.exe", "EpicWebHelper.exe"],
        "Steam": ["steam.exe"],
        "Battle": ["battle.net.exe"],
        "Riot": ["RiotClientUx.exe", "RiotClientServices.exe"]
    }

    def kill_process_and_children(process):
        """
        Internal helper to recursively kill a process and all of its child processes.
        """
        try:
            # Children Tasks
            children = process.children(recursive=True)
            for child in children:
                try:
                    child.kill()
                    debug_kill_adv_print(f"Killed child process: {child.name()} (PID: {child.pid})")
                except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                    debug_kill_adv_print(f"Error killing child process: {e}")
            # Main Parent Process
            process.kill()
            debug_kill_adv_print(f"Killed process: {process.name()} (PID: {process.pid})")
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            debug_kill_adv_print(f"Error accessing/killing process tree: {e}")

    # Search all running processes and compare their names
    for process_name in app_map.get(app_name, []):
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            try:
                if proc.info['name'].lower() == process_name.lower():
                    kill_process_and_children(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue  # Skip if a process disappeared or is restricted

class AppBlocker:
    """
    A class to monitor and terminate specified gaming applications based on external control signals.
    Designed for ESports or educational environments where gaming apps must be controlled remotely.

    Features:
    - Threaded background loop to continuously check for target apps.
    - Configurable kill list (via MQTT or other input).
    - Thread-safe status updates using a lock.
    - Graceful control via `enable` flag.

    To use:
    - Create an instance: `app_blocker = AppBlocker()`
    - Call `update_status(data_dict)` to update which apps to monitor and whether to enable killing.
    """

    def __init__(self):
        """
        Initializes internal flags, default status values, and starts the background killing thread.
        """
        self.app_status = {
            "Epic": False,
            "Steam": False,
            "Battle": False,
            "Riot": False
        }

        self.main_script_enabled = False            # By default, the kill loop is not run
        self.running = True                         # Allows for future graceful shutdown of the loop
        self.lock = threading.Lock()                # Prevents race conditions when updating status

        # Launch the background app-killing loop in a daemon thread
        self.kill_thread = threading.Thread(target=self.kill_apps_loop, daemon=True)
        self.kill_thread.start()

    def update_status(self, data):
        """
        Updates internal status dictionary from an external source, such as an MQTT message.
        """
        with self.lock:
            self.main_script_enabled = data.get("enable", False)
            for app in self.app_status:
                self.app_status[app] = data.get(app, False)

    def kill_apps_loop(self):
        """
        Background thread function that runs continuously.
        Depending on the KILL_LOOP_TIMEOUT seconds, it checks whether killing is enabled and, if so, attempts to kill listed apps.
        """
        while self.running:
            time.sleep(KILL_LOOP_TIMEOUT)
            with self.lock:
                if self.main_script_enabled:
                    self.check_and_kill_apps()

    def check_and_kill_apps(self):
        """
        Iterates through the app_status dictionary and attempts to kill any applications that are flagged True.
        """
        for app, should_kill in self.app_status.items():
            if should_kill:
                if DEBUG_KILL: print(f"KS: Killing {app}")
                kill_app(app)

    def stop(self):
        """
        Stops the background thread gracefully.
        """
        self.running = False

########################################################################################################


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
        window_title = getActiveWindowTitle()
        client.publish(f"PC/{MACHINE_ID}/app", window_title)

        # Current User
        client.publish(f"PC/{MACHINE_ID}/user", USERNAME)

        # Current Hostname
        client.publish(f"PC/{MACHINE_ID}/hostname", HOSTNAME)

        # Current Time (for detection of "Last Online @")
        client.publish(f"PC/{MACHINE_ID}/time", str(datetime.now()), 0, True)

        # Print the data if debugging
        if DEBUG_PUBLISH: print(f"\n----------------------\nData Sent: \n  CPU: {cpu_percent}% \n  Ram: {ram_percent}%\n  App: {window_title}\n  User: {USERNAME}\n  Time: {datetime.now()}\n----------------------\n")

        time.sleep(PUBLISH_TIMEOUT)


########################################################################################################


def on_connect(wsclient, userdata, flags, reason_code, properties):
    """
    Upon connecting to the WebSocket Server, subscribe to a topic to listen for specific messages. \n
    Other unused variables are needed in the function; otherwise there will be a positional arguments error
    """
    wsclient.subscribe("ESports/status")
    wsclient.subscribe(f"PC/{MACHINE_ID}/action")

    if reason_code=="Success":
        if WS_SHOW_CON_TOAST:
            def show_success_con_toast():
                toast(
                    "Yippee",
                    "Connected to Server",
                    icon=GoodIconPath,
                    audio='ms-winsoundevent:Notification.SMS'
                )
            threading.Thread(target=show_success_con_toast).start()
            # Threads automatically exit once the function is done
        print("Connected to WebSocket Server".center(CENTER_TEXT_WIDTH))
        if SHOW_WS_URL_PORT_STARTUP: print(f"{WS_SERVER}:{WS_PORT}".center(CENTER_TEXT_WIDTH))
        print(f"\n\n")
    else:
        toast(
            "Uh Oh",
            "Unable to connect to the Server for some reason",
            icon=ErrorIconPath,
            audio='ms-winsoundevent:Notification.Reminder',
            duration='short'
        )
        print("ERROR: Unable to connect to WebSocket Server".center(CENTER_TEXT_WIDTH))
        if SHOW_WS_URL_PORT_STARTUP: print(f"{WS_SERVER}:{WS_PORT}".center(CENTER_TEXT_WIDTH))
        print(f"\n\n")
        exit()

    debug_ws_connect_print(f"WS Client: {wsclient}")
    debug_ws_connect_print(f"Userdata: {userdata}")
    debug_ws_connect_print(f"flags: {flags}")
    debug_ws_connect_print(f"reason code: {reason_code}")
    debug_ws_connect_print(f"properties: {properties}")


########################################################################################################


# The callback for when the client receives a message
def on_message(wsclient, userdata, message):
    """
    Function that executes when a new message is received. \n
    First two arguments are needed, otherwise there will be a positional arguments error
    """
    topic = message.topic
    payload = message.payload.decode()

    if topic == f"PC/{MACHINE_ID}/action":
        handle_action(payload)

    elif topic == "ESports/status":
        handle_status_update(payload)

    debug_ws_mes_print(f"WS Client: {wsclient}")
    debug_ws_mes_print(f"Userdata: {userdata}")
    debug_ws_mes_print(f"Topic: {message.topic}")
    debug_ws_mes_print(f"Payload: {message.payload}")


def handle_action(action_str: str):
    """
    A more centralized and cleaner way of listing functions to execute based on the received action message
    :param action_str: Pass the type of action to be executed form the WebSocket Server. Can be given an argument with a colon. EX: shutdown:30
    """

    if ":" in action_str:
        action, arg = action_str.split(":", 1)
    else:
        action, arg = action_str, None

    debug_print(f"\n----------\nFull Action: {action_str}\nAction: {action}\nArg: {arg}\n----------\n")

    actions_map = {
        "none": lambda _: debug_print("\nNo Action to Do\n"),
        "test": lambda _: actions.show_test_notification(),
        "shutdown": lambda arg_timeout: actions.shutdown_pc(arg_timeout or DEFAULT_SHUTDOWN_TIMEOUT),
        "say": lambda arg_words: actions.say(arg_words),
        "MCEdu": lambda _: actions.run_MCEdu(),
        "ID": lambda _: actions.toastMachineID(),
        # "lock": lambda _: exec(StreamLock),
        # "unlock": lambda _: exec(StreamUnlock),
    }

    action_func = actions_map.get(action)
    if action_func:
        action_func(arg)
    else:
        debug_print(f"Unknown action: {action}")

    
def handle_status_update(payload: str):
    debug_status_print("Status Received")
    try:
        data = json.loads(payload)
        debug_status_print(data)
        app_blocker.update_status(data)
    except json.JSONDecodeError as e:
        debug_print(f"Failed to decode JSON: {e}")


########################################################################################################


# Initialize the AppBlocker
app_blocker = AppBlocker()

# Connect to the MQTT WebSockets broker
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, transport="websockets")
client.username_pw_set(username=WS_USERNAME, password=WS_PASSWORD)
if WS_USE_TLS: client.tls_set(ca_certs=None, certfile=None, keyfile=None) # Use system CA certificates (no ca_certs needed) based on config
client.on_message = on_message
client.on_connect = on_connect

try:
    client.connect(WS_SERVER, WS_PORT)
except Exception as e:
    print("ERROR: Unable to connect to WebSocket Server".center(CENTER_TEXT_WIDTH))
    print(f"Because: {e}".center(CENTER_TEXT_WIDTH))
    toast(
        "Uh Oh",
        f"Unable to connect to the Server for Data\nError: {e}",
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
publish_thread.join()