import time
import pyautogui

action_lists = []

def clicking():
    for action in action_lists:
        if action.mode == 'Time':
            time.sleep(int(action.delay))
            pyautogui.click(action.click_pos[0], action.click_pos[1])

        if action.mode == 'Screenshot':
            time.sleep(int(action.delay))
            # coordinates = [action.image_pos[0], action.image_pos[1], action.image_pos[0] + action.image.width, action.image_pos[1] + action.image.height]
            while True:
                try:
                    pos = pyautogui.locateOnScreen(action.image, confidence=0.8)
                    if pos:
                        break
                    time.sleep(0.1)
                except pyautogui.ImageNotFoundException:
                    time.sleep(0.1)

            pyautogui.click(action.click_pos[0], action.click_pos[1])

