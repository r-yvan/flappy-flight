"""
Flappy Flight - Persistence Module
Manages persistence mechanisms to ensure the client reconnects after reboot.
Currently supports Linux (autostart desktop entry).
"""

import os
import sys
import stat
import platform

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    APP_NAME, PERSISTENCE_NAME, AUTOSTART_DIR,
    INSTALL_DIR, AUTOSTART_ENTRY, LAUNCHER_SCRIPT,
    PROJECT_ROOT
)


def is_linux():
    """Check if running on Linux."""
    return platform.system() == "Linux"


def is_persistence_installed():
    """Check if persistence is already set up."""
    return os.path.exists(AUTOSTART_ENTRY)


def create_launcher_script():
    """
    Create a launcher shell script that starts the client on login.
    Stored in ~/.local/share/flappyflight/
    """
    os.makedirs(INSTALL_DIR, exist_ok=True)

    # Determine the python executable and the client module path
    python_path = sys.executable
    client_module = os.path.join(PROJECT_ROOT, "client", "client.py")

    script_content = f"""#!/bin/bash
# Flappy Flight Persistence Launcher
# This script is auto-generated. Do not modify.

# Wait for network to be available
sleep 10

# Start the Flappy Flight client in the background
cd "{PROJECT_ROOT}"
nohup "{python_path}" "{client_module}" > /dev/null 2>&1 &

exit 0
"""

    with open(LAUNCHER_SCRIPT, "w") as f:
        f.write(script_content)

    # Make executable
    st = os.stat(LAUNCHER_SCRIPT)
    os.chmod(LAUNCHER_SCRIPT, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)

    return LAUNCHER_SCRIPT


def create_autostart_entry():
    """
    Create a .desktop file in ~/.config/autostart/ for Linux persistence.
    """
    os.makedirs(AUTOSTART_DIR, exist_ok=True)

    desktop_content = f"""[Desktop Entry]
Type=Application
Name={APP_NAME}
Comment={APP_NAME} Background Service
Exec={LAUNCHER_SCRIPT}
Hidden=false
NoDisplay=true
X-GNOME-Autostart-enabled=true
StartupNotify=false
Terminal=false
"""

    with open(AUTOSTART_ENTRY, "w") as f:
        f.write(desktop_content)

    return AUTOSTART_ENTRY


def enable_persistence():
    """
    Enable persistence mechanism.
    Returns True if successful, False otherwise.
    """
    if not is_linux():
        print(f"  [!] Persistence is only supported on Linux.")
        print(f"  [i] Current OS: {platform.system()}")
        return False

    if is_persistence_installed():
        print("  [i] Persistence is already installed.")
        return True

    try:
        # Step 1: Create launcher script
        print("  [*] Creating launcher script...")
        launcher = create_launcher_script()
        print(f"  [✓] Launcher: {launcher}")

        # Step 2: Create autostart entry
        print("  [*] Creating autostart entry...")
        autostart = create_autostart_entry()
        print(f"  [✓] Autostart: {autostart}")

        print("\n  [✓] Persistence enabled successfully!")
        print("  [i] The client will auto-start on next login.")
        return True

    except PermissionError as e:
        print(f"  [✗] Permission denied: {e}")
        return False
    except Exception as e:
        print(f"  [✗] Failed to enable persistence: {e}")
        return False


def disable_persistence():
    """
    Remove persistence mechanism.
    Returns True if successful, False otherwise.
    """
    removed = []

    # Remove autostart entry
    if os.path.exists(AUTOSTART_ENTRY):
        try:
            os.remove(AUTOSTART_ENTRY)
            removed.append(f"Autostart entry: {AUTOSTART_ENTRY}")
        except Exception as e:
            print(f"  [✗] Failed to remove autostart entry: {e}")

    # Remove launcher script
    if os.path.exists(LAUNCHER_SCRIPT):
        try:
            os.remove(LAUNCHER_SCRIPT)
            removed.append(f"Launcher script: {LAUNCHER_SCRIPT}")
        except Exception as e:
            print(f"  [✗] Failed to remove launcher script: {e}")

    # Remove install directory if empty
    if os.path.exists(INSTALL_DIR):
        try:
            os.rmdir(INSTALL_DIR)
            removed.append(f"Install directory: {INSTALL_DIR}")
        except OSError:
            pass  # Directory not empty

    if removed:
        print("  [✓] Removed persistence components:")
        for item in removed:
            print(f"      - {item}")
        return True
    else:
        print("  [i] No persistence components found to remove.")
        return False


def check_persistence_status():
    """Print the current persistence status."""
    print(f"\n  Persistence Status for {APP_NAME}")
    print("  " + "─" * 40)

    if is_persistence_installed():
        print("  [✓] Status: ACTIVE")
        print(f"  [i] Autostart entry: {AUTOSTART_ENTRY}")
        if os.path.exists(LAUNCHER_SCRIPT):
            print(f"  [i] Launcher script: {LAUNCHER_SCRIPT}")
    else:
        print("  [✗] Status: NOT INSTALLED")

    print()


if __name__ == "__main__":
    check_persistence_status()
