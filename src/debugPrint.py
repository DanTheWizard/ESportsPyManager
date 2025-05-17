from config import DEBUG, DEBUG_STATUS, DEBUG_KILL_ADV, DEBUG_WS_CON, DEBUG_WS_MES

def debug_print(*args, **kwargs):
    """
    When DEBUG is set to true, it will allow printing Debugging Lines
    """
    if DEBUG:
        print("D: ", *args, **kwargs)

def debug_status_print(*args, **kwargs):
    """
    When DEBUG_STATUS is set to true, it will allow printing Debugging Lines on the recieveing status
    """
    if DEBUG_STATUS:
        print("D-Status: ", *args, **kwargs)

def debug_kill_adv_print(*args, **kwargs):
    """
    When DEBUG_KILL_ADV is set to true, it will allow printing Advanced Kill Debugging Status
    """
    if DEBUG_KILL_ADV:
        print("D-KillAdv: ", *args, **kwargs)


def debug_ws_connect_print(*args, **kwargs):
    """
    When DEBUG_WS_CON is set to true, it will allow printing some extra connection details when connecting to the WS server
    """
    if DEBUG_WS_CON:
        print("D-WS-CON: ", *args, **kwargs)


def debug_ws_mes_print(*args, **kwargs):
    """
    When DEBUG_WS_MES is set to true, it will allow printing some extra details when receiving data from WS Server
    """
    if DEBUG_WS_MES:
        print("D-WS-MES: ", *args, **kwargs)


if __name__ == "__main__":
    # Temporarily enable debug flags for testing
    DEBUG = True
    DEBUG_STATUS = True
    DEBUG_KILL_ADV = True
    DEBUG_WS_CON = True
    DEBUG_WS_MES = True

    # Import the functions (assuming they're in the same file or properly imported if split)
    debug_print("Test message for debug_print")
    debug_status_print("Test message for debug_status_print")
    debug_kill_adv_print("Test message for debug_kill_adv_print")
    debug_ws_connect_print("Test message for debug_ws_connect_print")
    debug_ws_mes_print("Test message for debug_ws_mes_print")
