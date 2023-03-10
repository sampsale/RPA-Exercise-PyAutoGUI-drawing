import pyautogui

def selectBrushTool():
    try:
        penciltool = pyautogui.locateOnScreen('referenceimages/brushtool.png', confidence=0.8)
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
        location = pyautogui.locateOnScreen('referenceimages/rectangletool.png', confidence=0.8)
        x, y, wid, hei = location
        x += wid//2
        y += hei//2
        pyautogui.moveTo(x, y, duration=0.1)
        pyautogui.click()
    except:
        print('Could not find square tool icon')
    


def selectTypeTool():
    try:
        typetool = pyautogui.locateOnScreen('referenceimages/typetool.png', confidence=0.8)
        # If the icon is found, set the mouse to the center of the icon and click
        x, y, wid, hei = typetool
        x += wid//2
        y += hei//2
        pyautogui.moveTo(x, y, duration=0.1)
        # Click twice to select
        pyautogui.click()
    except:
        print('Could not find brush icon')
