import pyautogui

def selectBrushTool():
    try:
        penciltool = pyautogui.locateOnScreen('brush.png')
        # If the icon is found, set the mouse to the center of the icon and click
        x, y, wid, hei = penciltool
        x += wid//2
        y += hei//2
        pyautogui.moveTo(x, y, duration=0.1)
        # Click twice to select
        pyautogui.doubleClick()
    except:
        print('Could not find brush icon')


def selectSquareTool():
    try:
        # Find the rectangle tool and click it
        location = pyautogui.locateOnScreen('rectangle.png')
        x, y, wid, hei = location
        x += wid//2
        y += hei//2
        pyautogui.moveTo(x, y, duration=0.1)
        pyautogui.click()
    except:
        print('Could not find square tool icon')
    