import paho.mqtt.client as mqtt                                                               # The WebSocket (and MQTT) library for connecting to a WS server
from config import *                                                                          # Import all variables and imports from config (cleaner structure)
from win11toast import toast                                                                  # Windows 11 Toast Notifications
from src.logo import CENTER_TEXT_WIDTH                                                            # Main width for text if to be centered



client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, transport="websockets")

def wsConnect():
    """Connect to the MQTT WebSockets broker"""
    client.username_pw_set(username=WS_USERNAME, password=WS_PASSWORD)
    if WS_USE_TLS: client.tls_set(ca_certs=None, certfile=None, keyfile=None) # Use system CA certificates (no ca_certs needed) based on config

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