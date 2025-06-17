import ctypes
import ctypes.wintypes

user32 = ctypes.WinDLL("user32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
wtsapi32 = ctypes.WinDLL("wtsapi32", use_last_error=True)
advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)

def get_active_session_id():
    return kernel32.WTSGetActiveConsoleSessionId()

def get_foreground_window_title():
    hwnd = user32.GetForegroundWindow()
    if hwnd == 0:
        return None
    length = user32.GetWindowTextLengthW(hwnd)
    if length == 0:
        return None
    buf = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buf, length + 1)
    return buf.value

def get_foreground_window_title_from_active_session():
    session_id = get_active_session_id()
    user_token = ctypes.wintypes.HANDLE()

    if not wtsapi32.WTSQueryUserToken(session_id, ctypes.byref(user_token)):
        raise ctypes.WinError(ctypes.get_last_error())

    if not advapi32.ImpersonateLoggedOnUser(user_token):
        raise ctypes.WinError(ctypes.get_last_error())

    try:
        title = get_foreground_window_title()
    finally:
        advapi32.RevertToSelf()
        kernel32.CloseHandle(user_token)

    return title if title else "No window title"

if __name__ == "__main__":
    try:
        print("Active Window Title (from active session):", get_foreground_window_title_from_active_session())
    except Exception as e:
        print("Failed:", str(e))
