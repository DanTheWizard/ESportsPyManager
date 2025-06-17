import ctypes
import ctypes.wintypes

WTS_CURRENT_SERVER_HANDLE = None
WTS_USER_NAME = 5
WTS_DOMAIN_NAME = 7

# Load DLLs
wtsapi32 = ctypes.WinDLL('wtsapi32.dll')
kernel32 = ctypes.WinDLL('kernel32.dll')

def get_logged_in_username():
    """
    This will return the username of the currently logged-in user
    despite whether the script is run with elevated privileges. \n
    Credit to ChatGPT for doing this (I have no idea what actually is happening)
    :return: Currently logged-in username
    """
    # Get active console session ID
    session_id = kernel32.WTSGetActiveConsoleSessionId()

    user_name_ptr = ctypes.c_void_p()
    user_len = ctypes.wintypes.DWORD()

    # Get username
    if wtsapi32.WTSQuerySessionInformationW(
        WTS_CURRENT_SERVER_HANDLE,
        session_id,
        WTS_USER_NAME,
        ctypes.byref(user_name_ptr),
        ctypes.byref(user_len)
    ):
        user_name = ctypes.wstring_at(user_name_ptr)
        wtsapi32.WTSFreeMemory(user_name_ptr)
    else:
        user_name = None

    if user_name:
        return f"{user_name}"
    else:
        return "Unknown_User"

if __name__ == "__main__":
    print(f"User: {get_logged_in_username()}")