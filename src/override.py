import os
import sys

# Determine current directory (works for a script and compiled exe)
BASE_DIR = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
OVERRIDE_PATH = os.path.join(BASE_DIR, "override.ini")

# Load simple key=value overrides into a dictionary
overrides = {}
if os.path.isfile(OVERRIDE_PATH):
    with open(OVERRIDE_PATH, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                overrides[key.strip()] = val.strip()

# Simple getter with type conversion
def get_override(variable, fallback, cast=str):
    raw = overrides.get(variable)
    if raw is None:
        return fallback
    try:
        if cast == bool:
            return raw.lower() in ("1", "true", "yes", "on")
        return cast(raw)
    except:
        return fallback
