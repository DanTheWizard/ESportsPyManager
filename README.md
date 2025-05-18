# ESportsPyManager (Previously PyAppKiller)

A Python-based client script that connects to a WebSocket server to send system telemetry and receive remote commands, specifically aimed at managing student activity on school machines. This project was designed with **educational institutions and ESports labs** in mind (which is where I am deploying this) — helping enforce focus by remotely disabling access to gaming applications during school hours.

> ⚙️ This project was made for fun, testing, deploying on custom-built computers, and practical experimentation. <br>
> It is actively evolving (whenever I can).

---

## ✨ Features

- 🔌 **WebSocket Communication**
    - Sends real-time data such as CPU usage, memory, focused window, and logged-in user.
<br><br>
- 🚫 **Remote Game Blocking**  
  - Receives `status` and `action` commands over MQTT to:
  - Kill pre-configured game launchers (Steam, Epic, Riot, Battle.net)
<br><br>
- 🖥️ Run remote custom actions like:
  - Shutdown (with an arg of a timer)
  - Say (A text to Speech)
  - Show a messagebox with the computer's ID
  - Show a test notification (useful to test if the connection is working)
  - And more per request of the ESports Lab Director
<br><br>
- 🧪 **Debug-Friendly Architecture**  
  Toggle debug output per feature with individual flags (`DEBUG_KILL`, `DEBUG_PUBLISH`, etc.).
<br><br>
- ⚙️ **Custom Runtime Overrides**  
  Use an optional `override.ini` to tweak behavior without modifying the original code — great for testing compiled `.exe` versions.


---


## 📦 Requirements

- Python 3.9 or higher
- Windows 10/11 (recommended for `win11toast`)
- Dependencies:
  - `paho-mqtt`
  - `psutil`
  - `pyautogui`
  - `python-dotenv`
  - `win11toast` (custom fork for Windows 11 native notifications)
  - Mark the `src` folder as a source root folder 


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