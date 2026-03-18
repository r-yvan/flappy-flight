#include <iostream>
#include <cstdlib>
#include <string>

/**
 * Flappy Flight - Quick Start Script (Windows)
 * This program serves as a launcher that executes 'python launcher.py'.
 * The Python logic handles virtual environment creation and dependency checks.
 */

int main() {
    std::cout << "[*] Starting Flappy Flight Launcher..." << std::endl;

    // Command to execute
    // Using "python launcher.py" because on Windows "python" is the standard command
    std::string command = "python launcher.py";

    // Execute the command
    int result = std::system(command.c_str());

    if (result != 0) {
        std::cerr << "[✗] Error: Failed to launch Flappy Flight." << std::endl;
        std::cerr << "    Ensure Python is installed and added to your PATH." << std::endl;
        return 1;
    }

    return 0;
}
