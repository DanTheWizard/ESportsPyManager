import subprocess
import re

def get_logged_in_username():
    """
    This will return the username of the currently logged-in user
    despite whether the script is run with elevated privileges.
    :return: Currently logged-in username
    """
    try:
        output = subprocess.check_output("quser", shell=True, text=True)
        lines = output.strip().splitlines()

        for line in lines:
            if line.strip().startswith('>'):
                # Remove the leading '>' and strip spaces
                cleaned_line = line[1:].strip()
                # Extract the username: it's the first column, which may contain spaces
                # So we find the point where multiple spaces start and split there
                match = re.match(r"(.+?)\s{2,}", cleaned_line)
                if match:
                    return match.group(1) or "Unknown_User"
        return "Unknown_User"
    except subprocess.CalledProcessError:
        return "Unknown_User"


if __name__ == "__main__":
    print(f"User: {get_logged_in_username()}")