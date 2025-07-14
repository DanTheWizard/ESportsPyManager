# ESportsPyManager (Previously PyAppKiller)

A Python-based client script that connects to a WebSocket server to send system telemetry and receive remote commands, specifically aimed at managing student activity on school machines. This project was designed with **educational institutions and ESports labs** in mind (which is where I am deploying this) — helping enforce focus by remotely disabling access to gaming applications during school hours.

> [!Warning]
> 🛠️ This is still in active development, and is made to work on my managed devices
>
> If you want to use it, **you will have to** modify some parts of it

> ⚙️ This project was made for fun, testing, deploying on custom-built computers, and practical experimentation.

> [!NOTE]  
> I am sharing the code to help others learn and adapt it for their own use cases 🙂

---

## ✨ Features

- 🔌 **WebSocket Communication**
    - Sends real-time data such as CPU usage, memory, focused window, and logged-in user.
<br><br>
- 🚫 **Remote Game Blocking**  
  - Receives `status` and `action` commands over WebSocket to block or unblock specific games.
  - Kill configured game launchers (Steam, Epic, Riot, Battle.net) based on a map in `map.py`
<br><br>
- 🖥️ Run remote custom actions like:
  - Shutdown (with an arg of a timer)
  - Say (A text to Speech)
  - Show a messagebox with the computer's ID
  - Show a test notification (useful to test if the connection is working)
  - And more per request of the ESports Lab Director
<br><br>
- 🧪 **Debug-Friendly Architecture**  
  - Toggle debug output per feature with individual flags (`DEBUG_KILL`, `DEBUG_PUBLISH`, etc.).
<br><br>
- ⚙️ **Custom Runtime Overrides**  
  - Use an optional `override.ini` to tweak behavior without modifying the original code — great for testing compiled `.exe` versions.


---

## 🧮 Admin Panel
You can find the admin panel to this tool [here](https://github.com/DanTheWizard/ESportsPyManager-AdminPanel):
- https://github.com/DanTheWizard/ESportsPyManager-AdminPanel

---

## 📦 Requirements

- Python 3.9 or higher _(Made with 3.13)_
- Windows 11 (recommended for `win11toast`)
- Dependencies (see `requirements.txt`):
  - `paho-mqtt` (for WebSocket communication)
  - `psutil`
  - `pyautogui`
  - `python-dotenv` (loading .env data)
  - `pyttsx3` (Text to Speech as one of the actions)
  - `win11toast` (custom fork for Windows 11 native notifications) 
  - `pyinstaller` (for compiling to .exe)
  - `pyinstaller_versionfile` (for version file generation for `pyinstaller`)


---


## 🔧 `win11toast` Build Requirement

The `win11toast` module **depends on the Windows SDK (`winsdk`) pip module** , which must be present to compile its native components.

To install and use it properly:

1. Install **[Visual Studio Community Edition](https://visualstudio.microsoft.com/vs/community/)**  
2. During installation, include:
   - Desktop development with C++
   - Windows SDK (10.0.x or higher)

Without this, running `pip install win11toast` will fail.


---


## 🔒 Example `.env`
```ini
WS_SERVER=example.com
WS_USERNAME=Username
WS_PASSWORD=Password
WS_PORT=8080
```


---


## 📄 Example `override.ini`

Place this file next to your compiled `.exe` or Python script to change behavior without editing code:

```ini
DEBUG=true
DEBUG_KILL=true
PUBLISH_TIMEOUT=2
DEFAULT_SHUTDOWN_TIMEOUT=15
SHOW_WS_URL_PORT_STARTUP=true
```
It is basically the same format config.py, but useful once the exe is compiled