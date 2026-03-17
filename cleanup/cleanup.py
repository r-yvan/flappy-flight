"""
Flappy Flight - Cleanup Tool
Removes all persistence mechanisms, terminates background processes,
and restores the system to its original state.
"""

import os
import sys
import subprocess
import signal
import platform

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    APP_NAME, PERSISTENCE_NAME, AUTOSTART_DIR,
    INSTALL_DIR, AUTOSTART_ENTRY, LAUNCHER_SCRIPT
)


def print_banner():
    """Display the cleanup tool banner."""
    banner = f"""
\033[33m╔══════════════════════════════════════════════╗
║                                              ║
║       {APP_NAME} Cleanup Tool               ║
║       System Restoration Utility             ║
║                                              ║
╚══════════════════════════════════════════════╝\033[0m
"""
    print(banner)


def remove_autostart_entry():
    """Remove the autostart desktop entry."""
    if os.path.exists(AUTOSTART_ENTRY):
        try:
            os.remove(AUTOSTART_ENTRY)
            print(f"  \033[32m[✓]\033[0m Removed autostart entry: {AUTOSTART_ENTRY}")
            return True
        except Exception as e:
            print(f"  \033[31m[✗]\033[0m Failed to remove autostart entry: {e}")
            return False
    else:
        print(f"  \033[33m[i]\033[0m No autostart entry found at: {AUTOSTART_ENTRY}")
        return True


def remove_launcher_script():
    """Remove the launcher script."""
    if os.path.exists(LAUNCHER_SCRIPT):
        try:
            os.remove(LAUNCHER_SCRIPT)
            print(f"  \033[32m[✓]\033[0m Removed launcher script: {LAUNCHER_SCRIPT}")
            return True
        except Exception as e:
            print(f"  \033[31m[✗]\033[0m Failed to remove launcher script: {e}")
            return False
    else:
        print(f"  \033[33m[i]\033[0m No launcher script found at: {LAUNCHER_SCRIPT}")
        return True


def remove_install_directory():
    """Remove the installation directory if empty."""
    if os.path.exists(INSTALL_DIR):
        try:
            # Remove any remaining files in the directory
            for root, dirs, files in os.walk(INSTALL_DIR, topdown=False):
                for name in files:
                    filepath = os.path.join(root, name)
                    os.remove(filepath)
                    print(f"  \033[32m[✓]\033[0m Removed file: {filepath}")
                for name in dirs:
                    dirpath = os.path.join(root, name)
                    os.rmdir(dirpath)

            os.rmdir(INSTALL_DIR)
            print(f"  \033[32m[✓]\033[0m Removed install directory: {INSTALL_DIR}")
            return True
        except Exception as e:
            print(f"  \033[31m[✗]\033[0m Failed to remove install directory: {e}")
            return False
    else:
        print(f"  \033[33m[i]\033[0m No install directory found at: {INSTALL_DIR}")
        return True


def kill_background_processes():
    """Find and terminate any running Flappy Flight background processes."""
    if platform.system() != "Linux":
        print(f"  \033[33m[i]\033[0m Process killing only supported on Linux.")
        return True

    killed = 0
    current_pid = os.getpid()

    try:
        # Find processes related to Flappy Flight client
        result = subprocess.run(
            ["pgrep", "-f", "flappyflight|client.py.*cybersec"],
            capture_output=True, text=True
        )

        if result.stdout.strip():
            pids = result.stdout.strip().split("\n")
            for pid_str in pids:
                try:
                    pid = int(pid_str.strip())
                    if pid == current_pid:
                        continue  # Don't kill ourselves

                    os.kill(pid, signal.SIGTERM)
                    killed += 1
                    print(f"  \033[32m[✓]\033[0m Terminated process PID: {pid}")
                except (ProcessLookupError, ValueError):
                    pass
                except PermissionError:
                    print(f"  \033[31m[✗]\033[0m Permission denied for PID: {pid_str}")

        if killed == 0:
            print(f"  \033[33m[i]\033[0m No running {APP_NAME} processes found.")
        else:
            print(f"  \033[32m[✓]\033[0m Terminated {killed} background process(es).")

    except FileNotFoundError:
        print(f"  \033[33m[i]\033[0m pgrep not available, skipping process check.")

    return True


def run_cleanup():
    """Run the full cleanup process."""
    print_banner()

    print("\033[36m  Starting cleanup process...\033[0m\n")
    print("  ─────────────────────────────────────────\n")

    # Step 1: Kill background processes
    print("  \033[36m[Step 1/4]\033[0m Terminating background processes...")
    kill_background_processes()
    print()

    # Step 2: Remove autostart entry
    print("  \033[36m[Step 2/4]\033[0m Removing autostart entry...")
    remove_autostart_entry()
    print()

    # Step 3: Remove launcher script
    print("  \033[36m[Step 3/4]\033[0m Removing launcher script...")
    remove_launcher_script()
    print()

    # Step 4: Remove install directory
    print("  \033[36m[Step 4/4]\033[0m Removing installation directory...")
    remove_install_directory()
    print()

    # Summary
    print("  ─────────────────────────────────────────\n")
    print("\033[32m  ╔══════════════════════════════════════════╗")
    print("  ║      Cleanup Complete!                   ║")
    print("  ║                                          ║")
    print("  ║  All Flappy Flight components have been      ║")
    print("  ║  removed from this system.               ║")
    print("  ║                                          ║")
    print("  ║  Your system has been restored to its     ║")
    print("  ║  original state.                         ║")
    print("  ╚══════════════════════════════════════════╝\033[0m\n")


if __name__ == "__main__":
    run_cleanup()
