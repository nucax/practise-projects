import pyautogui
import time

def lock_mouse_center():  
    screen_width, screen_height = pyautogui.size()
    center_x, center_y = screen_width // 2, screen_height // 2

    print("ctrl+c to stop.")

    try:
        while True:
            pyautogui.moveTo(center_x, center_y)
            time.sleep(0.01)  # don't put higher because it may fuck your gpu
    except KeyboardInterrupt:
        print("\nStopped mouse lock.")

if __name__ == "__main__":
    lock_mouse_center()
