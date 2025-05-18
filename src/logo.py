app_version = "1.1.5"
CENTER_TEXT_WIDTH = 100

def show_logo():
    """
    Shows a cool text ascii logo for this app, the version, who created it (Me), and what it does
    """
    # print(r"    _____ ____________________     ____  __.___.____    .____     _____________________  ".center(CENTER_TEXT_WIDTH))
    # print(r"   /  _  \\______   \______   \   |    |/ _|   |    |   |    |    \_   _____/\______   \ ".center(CENTER_TEXT_WIDTH))
    # print(r"  /  /_\  \|     ___/|     ___/   |      < |   |    |   |    |     |    __)_  |       _/ ".center(CENTER_TEXT_WIDTH))
    # print(r" /    |    \    |    |    |       |    |  \|   |    |___|    |___  |        \ |    |   \ ".center(CENTER_TEXT_WIDTH))
    # print(r" \____|__  /____|    |____|       |____|__ \___|_______ \_______ \/_______  / |____|_  / ".center(CENTER_TEXT_WIDTH))
    # print(r"         \/                               \/           \/       \/        \/         \/  ".center(CENTER_TEXT_WIDTH))
    print("")
    print(r"  ___________ ___________________________ ______________________________ ".center(CENTER_TEXT_WIDTH))
    print(r"  \_   _____//   _____/\______   \_____  \\______   \__    ___/   _____/ ".center(CENTER_TEXT_WIDTH))
    print(r"   |    __)_ \_____  \  |     ___//   |   \|       _/ |    |  \_____  \  ".center(CENTER_TEXT_WIDTH))
    print(r"   |        \/        \ |    |   /    |    \    |   \ |    |  /        \ ".center(CENTER_TEXT_WIDTH))
    print(r"  /_______  /_______  / |____|   \_______  /____|_  / |____| /_______  / ".center(CENTER_TEXT_WIDTH))
    print(r"          \/        \/                   \/       \/                 \/  ".center(CENTER_TEXT_WIDTH))
    # print("")
    print(r"     ___       __  ___                             ".center(CENTER_TEXT_WIDTH))
    print(r"    / _ \__ __/  |/  /__ ____  ___ ____ ____ ____  ".center(CENTER_TEXT_WIDTH))
    print(r"   / ___/ // / /|_/ / _ `/ _ \/ _ `/ _ `/ -_) __/  ".center(CENTER_TEXT_WIDTH))
    print(r"  /_/   \_, /_/  /_/\_,_/_//_/\_,_/\_, /\__/_/     ".center(CENTER_TEXT_WIDTH))
    print(r"       /___/                      /___/            ".center(CENTER_TEXT_WIDTH))
    print()
    print("WebSocket App".center(CENTER_TEXT_WIDTH))
    print(f"Version {app_version}".center(CENTER_TEXT_WIDTH))
    print()
    print("Developed by: DanTheWizard".center(CENTER_TEXT_WIDTH))
    print()
    print("This app is made to prevent some apps from being launched during school hours".center(CENTER_TEXT_WIDTH))
    print("based on the current config that is stored on a server".center(CENTER_TEXT_WIDTH))
    print()


if __name__ == "__main__":
    show_logo()