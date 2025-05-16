import subprocess
# Maybe Not Yet, might be a future Idea if I can figure out how to pass some stuff from main app.py (maybe a .env file)


def shutdown_pc(timeount: int):
    """
    Runs the shutdown command with the
    """
    #shutdown /s /t 60 /c "I'm tired, shutting down in 10 seconds"
    subprocess.run(
        ["shutdown", "/s", "/t", timeount, "/c", f"I'm tired, shutting down in {timeount} seconds"],
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