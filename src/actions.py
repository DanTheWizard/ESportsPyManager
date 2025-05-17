import subprocess
from win11toast import toast
# Maybe Not Yet, might be a future Idea if I can figure out how to pass some stuff from main app.py (maybe a .env file)


def shutdown_pc(timeout):
    """
    Runs the shutdown command with the set timeout
    """
    #shutdown /s /t 60 /c "I'm tired, shutting down in 10 seconds"
    subprocess.run(
        ["shutdown", "/s", "/t", str(timeout), "/c", f"I'm tired, shutting down in {timeout} seconds"],
        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
    )


def show_test_notification(icon_path):
    """
    Shows a simple test notification (useful only to see if the app received WS server command)
    """
    toast(
        "Test",
        "Test Successful",
        icon=icon_path,
        audio='ms-winsoundevent:Notification.SMS',
        button='Nice :)'
    )

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