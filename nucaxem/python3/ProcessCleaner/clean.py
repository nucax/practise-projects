#!/usr/bin/env python3
"""
Interactive Windows Task Killer
Closes all non-essential processes, except Windows system ones or whitelisted ones.
"""

import os
import psutil
from pathlib import Path
import time

PROTECTED_NAMES = {
    "system", "system idle process", "idle",
    "wininit.exe", "winlogon.exe", "csrss.exe", "smss.exe", "lsass.exe",
    "services.exe", "svchost.exe", "explorer.exe", "taskmgr.exe",
    "cmd.exe", "powershell.exe", "conhost.exe", "dwm.exe",
    "sihost.exe", "fontdrvhost.exe", "ctfmon.exe", "audiodg.exe",
    "lsm.exe"
}
PROTECTED_ACCOUNTS = {
    "nt authority\\system", "system",
    "nt authority\\localservice", "nt authority\\networkservice",
    "local service", "network service"
}
PROTECTED_PIDS = {0, 1, 2, 3, 4}

def load_whitelist(path="keep.txt"):
    names = set()
    p = Path(path)
    if not p.exists():
        print(f"No whitelist found at {path}. Skipping.")
        return names
    for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        names.add(s.lower())
    print(f"Loaded {len(names)} whitelisted process names.")
    return names

def should_protect(name, username, pid, whitelist):
    name = (name or "").lower()
    username = (username or "").lower()
    if pid in PROTECTED_PIDS:
        return True
    if name in PROTECTED_NAMES:
        return True
    if name in whitelist:
        return True
    if username in PROTECTED_ACCOUNTS:
        return True
    if pid == os.getpid():
        return True
    return False

def gather_processes():
    procs = []
    for p in psutil.process_iter(["pid", "name", "username"]):
        try:
            info = p.info
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
        procs.append(info)
    return procs

def terminate_process(pid):
    try:
        p = psutil.Process(pid)
        p.terminate()
        try:
            p.wait(timeout=2)
            return True, "terminated"
        except psutil.TimeoutExpired:
            p.kill()
            p.wait(timeout=2)
            return True, "killed"
    except psutil.NoSuchProcess:
        return False, "no such process"
    except psutil.AccessDenied:
        return False, "access denied"
    except Exception as e:
        return False, f"error: {e}"

def dry_run(whitelist):
    procs = gather_processes()
    to_kill = []
    for info in procs:
        pid = info.get("pid")
        name = info.get("name", "")
        user = info.get("username", "")
        if not should_protect(name, user, pid, whitelist):
            to_kill.append((pid, name, user))
    print("\n--- DRY RUN ---")
    print(f"Total: {len(procs)} | Protected: {len(procs)-len(to_kill)} | To Kill: {len(to_kill)}")
    for pid, name, user in to_kill[:30]:
        print(f" PID {pid:<6} {name:<30} user={user}")
    if len(to_kill) > 30:
        print(" ... and more.")
    input("\nPress Enter to return to main menu...")

def execute_kill(whitelist):
    procs = gather_processes()
    to_kill = []
    for info in procs:
        pid = info.get("pid")
        name = info.get("name", "")
        user = info.get("username", "")
        if not should_protect(name, user, pid, whitelist):
            to_kill.append((pid, name, user))
    print(f"\nTerminating {len(to_kill)} processes...\n")
    time.sleep(1)
    killed, failed = 0, 0
    for pid, name, user in to_kill:
        ok, msg = terminate_process(pid)
        if ok:
            print(f"[OK] {name} (PID {pid}) -> {msg}")
            killed += 1
        else:
            print(f"[FAIL] {name} (PID {pid}) -> {msg}")
            failed += 1
    print(f"\nDone. Killed: {killed}, Failed: {failed}\n")
    input("Press Enter to return to main menu...")

def main_menu():
    whitelist = set()
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=== WINDOWS TASK CLEANER ===")
        print("1. Load whitelist (keep.txt)")
        print("2. Show dry-run (list tasks that would be killed)")
        print("3. Terminate all non-essential tasks")
        print("4. Exit")
        print("============================")
        choice = input("Select an option (1-4): ").strip()

        if choice == "1":
            whitelist = load_whitelist("keep.txt")
            input("Press Enter to continue...")
        elif choice == "2":
            dry_run(whitelist)
        elif choice == "3":
            confirm = input("Are you sure? (y/N): ").lower()
            if confirm == "y":
                execute_kill(whitelist)
            else:
                print("Cancelled.")
                time.sleep(1)
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid input.")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
