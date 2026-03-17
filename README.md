# Flappy Flight 🐦

A Flappy Bird-inspired game combined with a controlled cybersecurity backdoor simulation for **educational purposes only**.

> ⚠️ **DISCLAIMER**: This project is for educational purposes only. Always test in a virtual machine. Never use on systems without explicit permission.

## 📋 Overview

Flappy Flight demonstrates how attackers may gain access to systems, maintain persistence, and interact remotely — while educating users about security risks and prevention techniques.

### Components

| Component              | Description                                               |
| ---------------------- | --------------------------------------------------------- |
| **Game (Client)**      | Flappy Bird game with cyber theme                         |
| **Listener (Server)**  | TCP listener that receives connections and sends commands |
| **Persistence Module** | Ensures auto-reconnection after system restart            |
| **Cleanup Tool**       | Removes all changes and restores the system               |

## 🔧 Installation

### Prerequisites

- Python 3.7+
- pip
- Linux OS (for persistence features)

### Setup

```bash
# Clone or navigate to the project directory
cd /path/to/cybersec

# Install dependencies
pip install -r requirements.txt
```

## 🚀 How to Run

### Step 1: Start the Listener (Attacker's Machine / Terminal 1)

```bash
cd /path/to/cybersec
python3 -m server.listener
```

This starts the TCP listener on `127.0.0.1:4444` and waits for incoming connections.

### Step 2: Launch the Game (Target's Machine / Terminal 2)

```bash
cd /path/to/cybersec
python3 launcher.py
```

This will:

1. Show a disclaimer and ask for consent
2. Check and install dependencies
3. Start a background client that connects to the listener
4. Optionally enable persistence
5. Launch the Flappy Bird game

### Step 3: Interact via the Listener

Once the client connects, you can type commands in the listener terminal:

```
Flappy Flight:user@hostname$ whoami
Flappy Flight:user@hostname$ hostname
Flappy Flight:user@hostname$ ls
Flappy Flight:user@hostname$ sysinfo
Flappy Flight:user@hostname$ uname -a
```

Type `help` to see all available commands.

## 🧹 Cleanup

To remove all Flappy Flight components from the system:

```bash
cd /path/to/cybersec
python3 -m cleanup.cleanup
```

This will:

- Terminate all background Flappy Flight processes
- Remove the autostart desktop entry
- Remove the launcher script
- Clean up the installation directory

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                       LAUNCHER                                │
│  (Consent → Dependencies → Client → Persistence → Game)     │
└───────────┬──────────────────────────────────────┬───────────┘
            │                                      │
            ▼                                      ▼
┌───────────────────────┐          ┌───────────────────────────┐
│    GAME MODULE        │          │     CLIENT MODULE         │
│                       │          │                           │
│  • Flappy Bird        │          │  • TCP Socket Connection  │
│  • Pygame Graphics    │          │  • System Info Gather     │
│  • Score Tracking     │          │  • Command Execution      │
│  • Collision Detection│          │  • Auto-Reconnect         │
│  (Main Thread)        │          │  (Background Thread)      │
└───────────────────────┘          └───────────┬───────────────┘
                                               │
                                    TCP Socket  │
                                   Connection   │
                                               ▼
                                   ┌───────────────────────────┐
                                   │    LISTENER (SERVER)      │
                                   │                           │
                                   │  • TCP Socket Listener    │
                                   │  • Interactive Shell      │
                                   │  • Client Info Display    │
                                   │  • Command Sending        │
                                   │  (Attacker's Machine)     │
                                   └───────────────────────────┘

┌───────────────────────┐          ┌───────────────────────────┐
│  PERSISTENCE MODULE   │          │    CLEANUP TOOL           │
│                       │          │                           │
│  • Autostart Entry    │  ◄────►  │  • Remove Autostart       │
│  • Launcher Script    │          │  • Kill Processes         │
│  • Auto-Reconnect     │          │  • Restore System         │
└───────────────────────┘          └───────────────────────────┘
```

## 📁 Project Structure

```
cybersec/
├── README.md                  # This file
├── requirements.txt           # Python dependencies
├── config.py                  # Shared configuration
├── launcher.py                # Main entry point
├── game/
│   ├── __init__.py
│   └── flappy_bird.py         # Flappy Bird game (Pygame)
├── client/
│   ├── __init__.py
│   ├── dependency_checker.py  # Dependency checker & installer
│   ├── client.py              # Reverse shell client
│   └── persistence.py         # Persistence mechanisms
├── server/
│   ├── __init__.py
│   └── listener.py            # TCP listener / command center
└── cleanup/
    ├── __init__.py
    └── cleanup.py             # System restoration tool
```

## 🎮 Game Controls

| Key               | Action                    |
| ----------------- | ------------------------- |
| `SPACE` / `Click` | Flap (make the bird jump) |
| `ESC`             | Exit the game             |
| `SPACE` / `ENTER` | Restart after game over   |

## 🔒 Security & Ethical Considerations

1. **User Consent**: The system requires explicit user consent ("I AGREE") before execution
2. **Safe Commands Only**: Only predefined, non-destructive commands are allowed
3. **Transparency**: Users are informed about what the program does before running
4. **Cleanup Available**: A dedicated cleanup tool removes all traces
5. **Educational Only**: Must be tested in a controlled virtual machine environment
6. **No Data Theft**: No personal files are accessed or exfiltrated
7. **Logged Actions**: All operations are transparent and reversible

## 👥 Team

Rwanda Coding Academy - Cybersecurity Course Assignment

## 📄 License

For educational purposes only. Not for production or malicious use.
