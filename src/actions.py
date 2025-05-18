import subprocess
import tkinter as tk
from win11toast import toast
from ws_connect import client
from tkinter import messagebox
from config import MACHINE_ID, GoodIconPath


def clean_action():
    """
    Sets the action to none after executing an action (to keep it clean)
    """
    client.publish(f"PC/{MACHINE_ID}/action", "none")


def shutdown_pc(timeout):
    """
    Runs the shutdown command with the set timeout
    """
    #shutdown /s /t 60 /c "I'm tired, shutting down in 10 seconds"
    subprocess.run(
        ["shutdown", "/s", "/t", str(timeout), "/c", f"I'm tired, shutting down in {timeout} seconds"],
        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
    )
    clean_action()


def show_test_notification():
    """
    Shows a simple test notification (useful only to see if the app received WS server command)
    """
    toast(
        "Test",
        "Test Successful",
        icon=GoodIconPath,
        audio='ms-winsoundevent:Notification.SMS',
        button='Nice :)'
    )
    clean_action()

def say(words):
    """
    Shows a simple test notification (useful only to see if the app received WS server command)
    """
    toast(
        "Saying",
        f"{words}",
        audio='ms-winsoundevent:Notification.SMS',
        dialogue=f'{words}',
    )
    clean_action()


def messageboxMachineID():
    """
    Shows a messagebox with the device's fingerprint
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showinfo("Machine Identity", f"  This is this computers identifier: \n  {MACHINE_ID}")
    clean_action()

# Was manually requested
def run_MCEdu():
    """
    Runs Minecraft Education Edition
    """
    print("\nLaunching MCEdu\n")
    # exec("os.system('start minecraftedu://')")
    subprocess.run(
        ["start", "minecraftedu://"],
        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
    )
    clean_action()