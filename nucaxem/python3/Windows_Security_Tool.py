# .com/nucax
import os
import subprocess
import webbrowser
import keyboard
import sys
import time

KEY_LIST = {
    'F1': 'Show this key list',
    'F2': 'Open cmd (terminal)',
    'F3': 'Open PowerShell',
    'F4': 'Open Registry Editor',
    'F5': 'Open Task Manager',
    'F6': 'Log out (sign out)',
    'F7': 'Shut down the PC',
    'F8': 'Restart the PC',
    'F9': 'Open https://github.com/nucax'
}

def show_keys():
    print('\n--- Key list ---')
    for k, v in KEY_LIST.items():
        print(f'{k}: {v}')
    print('----------------\n')

def open_cmd():
    subprocess.Popen(['cmd.exe'], shell=False)

def open_powershell():
    subprocess.Popen(['powershell.exe'], shell=False)

def open_regedit():
    subprocess.Popen(['regedit.exe'], shell=False)

def open_taskmgr():
    subprocess.Popen(['taskmgr.exe'], shell=False)

def logout():
    os.system('shutdown -l')

def shutdown():
    os.system('shutdown /s /t 0')

def restart():
    os.system('shutdown /r /t 0')

def open_github():
    webbrowser.open('https://github.com/nucax', new=2)

HOTKEYS = {
    'f1': show_keys,
    'f2': open_cmd,
    'f3': open_powershell,
    'f4': open_regedit,
    'f5': open_taskmgr,
    'f6': logout,
    'f7': shutdown,
    'f8': restart,
    'f9': open_github
}

def register_hotkeys():
    for key, func in HOTKEYS.items():
        keyboard.add_hotkey(key, func)

def main():
    if os.name != 'nt':
        sys.exit()
    register_hotkeys()
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()
