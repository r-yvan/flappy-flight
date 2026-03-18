"""
Flappy Flight - Dependency Checker
Checks and installs required dependencies for the Flappy Flight system.
"""

import subprocess
import sys
import importlib
import os


def is_in_venv():
    """Check if the current process is running inside a virtual environment."""
    return sys.prefix != sys.base_prefix


def get_venv_python():
    """Get the path to the python executable in the virtual environment."""
    if os.name == 'nt':  # Windows
        return os.path.join(".env", "Scripts", "python.exe")
    else:  # Linux/Mac
        return os.path.join(".env", "bin", "python")


def ensure_venv():
    """
    Ensures that a virtual environment exists and is being used.
    If not, it creates one and signals that a restart is needed.
    Returns:
        bool: True if we are in the venv and ready, False if a restart is needed.
    """
    venv_dir = ".env"
    
    # 1. Check if venv exists
    if not os.path.exists(venv_dir):
        print(f"\n\033[33m[*] Creating an isolated Virtual Environment in {venv_dir}...\033[0m")
        
        # OS-specific python command for venv creation
        python_cmd = "python" if os.name == 'nt' else "python3"
        
        try:
            subprocess.check_call([python_cmd, "-m", "venv", venv_dir])
            print("\033[32m[✓] Virtual Environment created successfully!\033[0m")
            
            # Since we just created it, we definitely need to install requirements
            install_requirements(get_venv_python())
        except subprocess.CalledProcessError:
            print(f"\033[31m[✗] Failed to create virtual environment using {python_cmd}.\033[0m")
            if os.name != 'nt':
                print("    Try: sudo apt-get install python3-venv")
            sys.exit(1)

    # 2. Check if we are already running inside the venv
    if not is_in_venv():
        return False  # Indicate restart needed
        
    return True


def install_requirements(venv_python=None):
    """Install dependencies from requirements.txt."""
    if venv_python is None:
        venv_python = sys.executable

    requirements_file = "requirements.txt"
    if os.path.exists(requirements_file):
        print(f"\033[33m[*] Installing dependencies from {requirements_file}...\033[0m")
        try:
            subprocess.check_call(
                [venv_python, "-m", "pip", "install", "-r", requirements_file, "--quiet"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            print("\033[32m[✓] Dependencies installed!\033[0m")
            return True
        except subprocess.CalledProcessError:
            print("\033[31m[✗] Failed to install dependencies.\033[0m")
            return False
    return True


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
    if not ensure_venv():
        venv_py = get_venv_python()
        print(f"[*] Restarting under virtual environment: {venv_py}")
        os.execv(venv_py, [venv_py] + sys.argv)
    else:
        check_dependencies()
