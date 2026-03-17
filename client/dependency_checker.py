"""
Flappy Flight - Dependency Checker
Checks and installs required dependencies for the Flappy Flight system.
"""

import subprocess
import sys
import importlib


def check_module(module_name):
    """Check if a Python module is installed."""
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False


def install_module(module_name, pip_name=None):
    """Install a Python module using pip."""
    pip_name = pip_name or module_name
    print(f"  [*] Installing {pip_name}...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", pip_name, "--quiet"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(f"  [✓] {pip_name} installed successfully.")
        return True
    except subprocess.CalledProcessError:
        print(f"  [✗] Failed to install {pip_name}.")
        return False


# Required dependencies: (module_name, pip_name)
REQUIRED_DEPS = [
    ("pygame", "pygame"),
]


def check_dependencies():
    """
    Check all required dependencies and install missing ones.
    Returns True if all dependencies are satisfied, False otherwise.
    """
    print("\n╔════════════════════════════════════════════╗")
    print("║      Flappy Flight - Dependency Checker       ║")
    print("╚════════════════════════════════════════════╝\n")

    all_ok = True

    for module_name, pip_name in REQUIRED_DEPS:
        if check_module(module_name):
            print(f"  [✓] {pip_name} is already installed.")
        else:
            print(f"  [!] {pip_name} is NOT installed.")
            success = install_module(module_name, pip_name)
            if not success:
                all_ok = False

    # Check Python version
    py_version = sys.version_info
    print(f"\n  [i] Python version: {py_version.major}.{py_version.minor}.{py_version.micro}")
    if py_version.major < 3 or (py_version.major == 3 and py_version.minor < 7):
        print("  [✗] Python 3.7+ is required!")
        all_ok = False
    else:
        print("  [✓] Python version is compatible.")

    if all_ok:
        print("\n  [✓] All dependencies are satisfied!\n")
    else:
        print("\n  [✗] Some dependencies could not be installed.")
        print("  [i] Try: pip install -r requirements.txt\n")

    return all_ok


if __name__ == "__main__":
    check_dependencies()
