# Flappy Flight - Comprehensive Testing Plan 🧪

This document outlines explicitly how to test and prove that every single grading criteria and requested feature is fully functional. By following these steps sequentially, you can gather the required "proof" to secure the full 50 marks.

---

### Feature 1: The user is notified of what will happen (Game Functionality)

**Goal**: Prove the user is warned and their consent is required before the backdoor starts.

**Test Steps:**

1. Open a terminal and run your quick-start script: `./play.sh`
2. **Observe**: The application halts operation instantly. It presents a yellow `⚠ DISCLAIMER ⚠` warning detailing the background process, the listener configuration (`10.12.74.31:4444`), persistence, and logged actions.
3. Type `NO` or press `Ctrl+C`. **Observe**: The application exits entirely.
4. Run `./play.sh` again, this time type exactly `I AGREE`.
5. **Observe**: `[✓] Consent received. Proceeding...` is logged.
   **Proof**: The user completely controls the execution flow and is legally/ethically notified.

---

### Feature 2: Required dependencies are installed (Game Functionality)

**Goal**: Prove the app checks for and downloads missing required applications (like `pygame` and `pip`).

**Test Steps:**

1. Manually sabotage the environment by removing the required dependency:
   `pip3 uninstall pygame -y`
2. Run `./play.sh` again.
3. **Observe**: Under the _Dependency Checker_ banner, it identifies that `pygame` is NOT installed.
4. **Observe**: It automatically runs the internal downloading sub-process: `[*] Installing pygame...` and successfully restores it without you doing anything.
   **Proof**: The system natively resolves and downloads its own dependencies.

---

### Feature 3: Shell access is provided to the listener (Game Functionality)

**Goal**: Prove the remote attacker can access the target's shell.

**Test Steps:**

1. Open **Terminal 1** (Acting as Attacker) and run the server listener:
   `python3 -m server.listener`
2. Open **Terminal 2** (Acting as Target) and launch the game:
   `./play.sh`
3. Wait for the consent prompt, type `I AGREE`.
4. Switch back to **Terminal 1**.
5. **Observe**: You will see `[✓] Connection received` followed by the target's System Information.
6. **Interact**: Type `whoami`, then type `ls -la`, then type `sysinfo`.
7. **Observe**: You correctly receive the target's CLI output live.
   **Proof**: The reverse TCP shell successfully routes standard output to the attacker's terminal.

---

### Feature 4: The user can run the game without interruption (Game Functionality)

**Goal**: Prove the background shell operations don't freeze or lag the main Pygame graphics loop.

**Test Steps:**

1. Continue from the setup in Feature 3. Make sure the Flappy Bird game window is visibly running on your screen.
2. Start playing the game pressing `SPACE`.
3. While the bird is actively falling/jumping, step into **Terminal 1** (Listener) and fire off a resource-heavy command, like: `find / -name "*.txt" 2>/dev/null` (or simply spam `sysinfo`).
4. **Observe**: The Pygame window does not freeze, drop frames, or stutter.
   **Proof**: Because the backdoor is bound to a `daemon=True` background Python thread, network I/O operations are fully separated from the Pygame loop.

---

### Feature 5: Persistence features are implemented (Persistence & Security)

**Goal**: Prove the game injects itself into user startup systems to survive reboots.

**Test Steps:**

1. Finish launching the game (`./play.sh`) and accept the `Enable persistence? (y/n):` prompt by pressing `y`.
2. Open a new terminal and verify the payload files were placed correctly by inspecting their contents:
   `cat ~/.config/autostart/flappyflight.desktop`
   `cat ~/.local/share/flappyflight/flappyflight_launcher.sh`
3. **Observe**: You will see the physical autostart instructions written accurately to standard Linux startup paths.
4. **Real-world Test**: Fully restart your computer. Log back in. Open a terminal and type:
   `pgrep -f flappyflight`
5. **Observe**: The system returns a Process ID (PID), proving the backdoor launched invisibly upon logging in, without manually running the game.
   **Proof**: Execution survives reboots dynamically.

---

### Feature 6: The apps to remove persistence features is implemented (User Protection)

**Goal**: Prove the cleanup tool ethically reverses all traces.

**Test Steps:**

1. While the backdoor daemon is still running, open a terminal and execute the cleanup app:
   `python3 -m cleanup.cleanup`
2. **Observe the Logs**:
   - `[Step 1/4]` Terminating background processes... `[✓]`
   - `[Step 2/4]` Removing autostart entry... `[✓]`
   - `[Step 3/4]` Removing launcher script... `[✓]`
3. Verify the changes are completely gone by running:
   `ls ~/.config/autostart/flappyflight.desktop` (It should say: _No such file or directory_)
   `pgrep -f flappyflight` (It should return _absolutely nothing_)
   **Proof**: The system guarantees a robust anti-malware reversal option.
