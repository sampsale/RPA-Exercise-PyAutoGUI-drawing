import pyautogui
from toolselectors import selectBrushTool
import random
import time

# Ruin canvas by writing the number on squares
def write_number_on_square(number, squarelocation, squaresize):
    # move the mouse to the center of the square
    pyautogui.moveTo(squarelocation[0] + squaresize//2, squarelocation[1] + squaresize//2)
    pyautogui.doubleClick()
    pyautogui.write(str(number), interval=0.1)
    # Move to square 0,0 and click to deselect
    pyautogui.moveTo(squarelocation[0], squarelocation[1])
    pyautogui.click()

# Ruin canvas by drawing the numbers on squares
def draw_number_on_canvas(number, squarelocation, squaresize):
    print(squarelocation)
    
    # define the numbers as a list of coordinates
    numbers_to_draw = [
        ((100, 100), (200, 100), (200, 200), (100, 200), (100, 100)),  # 0
        ((150, 100), (150, 200)),  # 1
        ((100, 100), (200, 100), (200, 150),
         (100, 150), (100, 200), (200, 200)),  # 2
        ((100, 100), (200, 100), (200, 150), (100, 150),
         (200, 150), (200, 200), (100, 200)),  # 3
        ((100, 100), (100, 150), (200, 150), (200, 100), (200, 200)),  # 4
        ((200, 100), (100, 100), (100, 150),
         (200, 150), (200, 200), (100, 200)),  # 5
    ]

    # move the mouse to the starting position of the number
    pyautogui.moveTo(squarelocation[0] + numbers_to_draw[number][0][0] - squaresize//2,
                     squarelocation[1] + numbers_to_draw[number][0][1] - squaresize//2)

    # click and drag the mouse to draw the number
    pyautogui.mouseDown()
    # loop through the coordinates and draw the number
    for point in numbers_to_draw[number][1:]:
        pyautogui.moveTo(squarelocation[0] - squaresize//2 +
                         point[0], squarelocation[1] - squaresize//2 + point[1])
        time.sleep(0.05)

    pyautogui.mouseUp()

# Ruin canvas by drawing lines on it
def messUpTheCanvas(canvaslocation, squaresize):
    # Get the canvas in the same way we got the squares
    safetymargins = 10
    x, y = canvaslocation[0], canvaslocation[1]
    maxx = canvaslocation[2] - squaresize - safetymargins
    maxy = canvaslocation[3]

    # Select brush tool
    selectBrushTool()
    # Move to the top-left corner of the canvas
    pyautogui.moveTo(x + safetymargins, y + safetymargins)

    # Draw lines from left to right, covering the whole screen
    # Subtract randomint(5-15) from range step to make sure all squares are covered (in rare borderline cases the lines would perfectly overlap with the squares's borders, messing up the image recognition). Randomness also makes sure the lines are not identical if this function has to be run more than once (if squares are still detected).
    randomness = random.randint(5,15)
    for i in range(safetymargins, maxy, (squaresize-randomness)):
        pyautogui.dragTo(maxx + safetymargins + squaresize, y + i, button='left')
        # If the end of the canvas is reached, break the loop
        if y+i > maxy:
            break
        pyautogui.moveTo(x + safetymargins, y + i + squaresize-randomness)

    