import src.actions as actions                                         # Set of actions to do based on received WebSocket action string
from config import DEFAULT_SHUTDOWN_TIMEOUT                            # Default shutdown timeout from config

APPS_LIST = {
    "Epic":   False,
    "Steam":  False,
    "Battle": False,
    "Riot":   False,
    "MCJava": False,
    "MCEdu":  False
} ; "List of all the apps to kill, with a default value of whether to kill or not (False = do not kill, True = kill)"


APP_MAP = {
    "Epic":   ["EpicGamesLauncher.exe", "EpicWebHelper.exe"],
    "Steam":  ["steam.exe"],
    "Battle": ["battle.net.exe"],
    "Riot":   ["RiotClientUx.exe", "RiotClientServices.exe"],
    "MCJava": ["javaw.exe", "MinecraftLauncher.exe"],
    "MCEdu":  ["Minecraft.Windows.exe"]
} ; "Map of all the apps to kill, with the first item being the main app from APP_LIST and the rest being the exe names"

ACTION_MAP = {
    "none":     lambda _: actions.none_action(),
    "test":     lambda _: actions.show_test_notification(),
    "MCEdu":    lambda _: actions.run_MCEdu(),
    "MCJava":   lambda _: actions.run_MCJava(),
    "ID":       lambda _: actions.messageboxMachineID(),
    "reboot":   lambda _: actions.reboot_pc(),
    "shutdown": lambda arg_timeout: actions.shutdown_pc(arg_timeout or DEFAULT_SHUTDOWN_TIMEOUT),
    "say":      lambda arg_words:   actions.say(arg_words),
    # "lock": lambda _: exec(StreamLock),
    # "unlock": lambda _: exec(StreamUnlock),
}