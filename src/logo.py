app_version = "1.2.0"
CENTER_TEXT_WIDTH = 100

def printc(text: str = ""):
    """
    Prints the given text centered within the defined width.

    Args:
        text (str): The text to print. Defaults to an empty string for spacing.
    """
    print(text.center(CENTER_TEXT_WIDTH))

def show_logo():
    """
    Displays an ASCII art logo along with version info, author, and app purpose.
    """
    logo_lines = [
        r"  ___________ ___________________________ ______________________________ ",
        r"  \_   _____//   _____/\______   \_____  \\______   \__    ___/   _____/ ",
        r"   |    __)_ \_____  \  |     ___//   |   \|       _/ |    |  \_____  \  ",
        r"   |        \/        \ |    |   /    |    \    |   \ |    |  /        \ ",
        r"  /_______  /_______  / |____|   \_______  /____|_  / |____| /_______  / ",
        r"          \/        \/                   \/       \/                 \/  ",
        r"     ___       __  ___                             ",
        r"    / _ \__ __/  |/  /__ ____  ___ ____ ____ ____  ",
        r"   / ___/ // / /|_/ / _ `/ _ \/ _ `/ _ `/ -_) __/  ",
        r"  /_/   \_, /_/  /_/\_,_/_//_/\_,_/\_, /\__/_/     ",
        r"       /___/                      /___/            ",
        "",
        "WebSocket App",
        f"Version {app_version}",
        "",
        "Developed by: DanTheWizard",
        "",
        "This app is made to prevent some apps from being launched during school hours",
        "based on the current config that is stored on a server",
        ""
    ]

    for line in logo_lines:
        printc(line)



if __name__ == "__main__":
    show_logo()