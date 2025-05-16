import subprocess

def get_logged_in_username():
    """
    This will return the username of the currently logged-in user
    despite whether the script is run with elevated privileges.
    :return: Currently logged-in username
    """
    try:
        output = subprocess.check_output(
            ['powershell', '-Command',
             'Get-WmiObject -Class Win32_ComputerSystem | Select-Object -ExpandProperty UserName'],
            text=True
        )
        full_user = output.strip()
        if '\\' in full_user:
            return full_user.split('\\')[1]  # Extract just the username part
        return full_user or "Unknown_User"
    except subprocess.CalledProcessError:
        return "Unknown_User"


if __name__ == "__main__":
    print(f"User: {get_logged_in_username()}")