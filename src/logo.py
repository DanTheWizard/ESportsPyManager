app_version = "1.0.7"
WIDTH = 89

def show_logo():
    """
    Shows a cool text ascii logo for this app, the version, who created it (Me), and what it does
    """
    print(r"    _____ ____________________     ____  __.___.____    .____     _____________________  ")
    print(r"   /  _  \\______   \______   \   |    |/ _|   |    |   |    |    \_   _____/\______   \ ")
    print(r"  /  /_\  \|     ___/|     ___/   |      < |   |    |   |    |     |    __)_  |       _/ ")
    print(r" /    |    \    |    |    |       |    |  \|   |    |___|    |___  |        \ |    |   \ ")
    print(r" \____|__  /____|    |____|       |____|__ \___|_______ \_______ \/_______  / |____|_  / ")
    print(r"         \/                               \/           \/       \/        \/         \/  ")
    print()
    print("WebSocket App".center(WIDTH))
    print(f"Version {app_version}".center(WIDTH))
    print()
    print("Developed by: DanTheWizard".center(WIDTH))
    print()
    print("This app is made to prevent some apps from being launched during school hours".center(WIDTH))
    print("based on the current config that is stored on a server".center(WIDTH))
    print()



if __name__ == "__main__":
    show_logo()