import subprocess
import threading                               # Used to run multiple functions at once
import tkinter as tk
from win11toast import toast
from ws_connect import client
from tkinter import messagebox
from config import MACHINE_ID, GoodIconPath
import pyttsx3


# Every action must be created in a separate thread as it will freeze the publishing


def clean_action():
    """
    Sets the action to none after executing an action (to keep it clean)
    """
    client.publish(f"PC/{MACHINE_ID}/action", "none")


def shutdown_pc(timeout):
    """
    Runs the shutdown command with the set timeout
    """
    def run():
        try:
            #shutdown /s /t 60 /c "I'm tired, shutting down in 10 seconds"
            subprocess.run(
                ["shutdown", "/s", "/t", str(timeout), "/c", f"I'm tired, shutting down in {timeout} seconds"],
                shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
            )
        except Exception as e:
            print(f"Error in shutdown_pc(): {e}")
        finally:
            clean_action()
    threading.Thread(target=run).start()


def show_test_notification():
    """
    Shows a simple test notification (useful only to see if the app received WS server command)
    """
    def run():
        try:
            toast(
                "Test",
                "Test Successful",
                icon=GoodIconPath,
                audio='ms-winsoundevent:Notification.SMS',
                button='Nice :)'
            )
        except Exception as e:
            print(f"Error in show_test_notification(): {e}")
        finally:
            clean_action()
    threading.Thread(target=run).start()

def say(words):
    """
    Shows a simple test notification (useful only to see if the app received WS server command)
    """
    def run():
        try:
            engine = pyttsx3.init()
            engine.setProperty('volume', 1.0)          # setting up volume level  between 0 and 1
            voices = engine.getProperty('voices')      # getting details of current voice
            engine.setProperty('voice', voices[0].id)  # changing index, changes voices. o for male, 1 for female
            engine.say(f"{words}")
            engine.runAndWait()
            engine.stop()
        except Exception as e:
            print(f"Error in say(): {e}")
        finally:
            clean_action()
    threading.Thread(target=run).start()



def messageboxMachineID():
    """
    Shows a messagebox with the device's fingerprint
    """
    def run():
        try:
            engine = pyttsx3.init()
            engine.setProperty('volume', 1.0)
            engine.say(f"This computer is {MACHINE_ID}")
            engine.runAndWait()
            engine.stop()

            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showinfo("Machine Identity", f"  This is this computers identifier: \n  {MACHINE_ID}")
        except Exception as e:
            print(f"Error in messageboxMachineID(): {e}")
        finally:
            clean_action()
    threading.Thread(target=run).start()


# Was manually requested
def run_MCEdu():
    """
    Runs Minecraft Education Edition
    """
    def run():
        try:
            print("\nLaunching MCEdu\n")
            # exec("os.system('start minecraftedu://')")
            subprocess.run(
                ["start", "minecraftedu://"],
                shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
            )
        except Exception as e:
            print(f"Error in run_MCEdu(): {e}")
        finally:
            clean_action()
    threading.Thread(target=run).start()