import pyautogui
import random
import math
from toolselectors import selectBrushTool, selectSquareTool




# Activate failsafe to interrupt if needed
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5
# Squaresize for squares.. change this if you want larger or smaller ones
squaresize = 50
# Init these for pyautogui
screenwidth, screenheight = pyautogui.size()


# Simplest strategy to open the Paint app
def openMSPaint():
    # Press windows key, type paint, and press enter
    pyautogui.press('win')
    pyautogui.typewrite('Paint', 0.1)
    pyautogui.press('enter')
    drawSquares()

# Open Paint with image recognition. WILL ONLY WORK ON DARKMODE WINDOWS and therefore not optimal!!!
def openMSPaintWithImageRecognition():
    # Press windows key, type paint
    pyautogui.press('win')
    pyautogui.typewrite('Paint', 0.1)
    # Try to find the paint icon
    try:
        location = pyautogui.locateOnScreen('paint.png')
        # If the icon is found, set the mouse to the center of the icon and click
        x, y, wid, hei = location
        x += wid//2
        y += hei//2
        pyautogui.moveTo(x, y, duration=0.1)
        pyautogui.click()
    except:
        print('Could not find Paint icon')
    drawSquares()


def locateCanvas():
    # Locate canvas
    location = pyautogui.locateOnScreen('canvas.png')
    return location


def generateSquares(canvaslocation):

    # Init squaresize and list of existing squares. Also get the amount of squares (2-5)
    squarestartpoints = []
    amount_of_squares = random.randrange(2, 6)

    safetymargins = 10
    # Get the possible locations for the squares
    # Safetymargins are added to prevent the squares from being drawn right at the border of the canvas
    x, y = canvaslocation[0], canvaslocation[1]
    maxx = canvaslocation[2] - squaresize*2 - safetymargins
    maxy = canvaslocation[3] - squaresize*2 - safetymargins

    # Console logs for debugging
    print('Number of squares:', amount_of_squares)
    print('Canvas specs', canvaslocation)
    print('Screen specs', screenwidth, screenheight)
    print('Max x', maxx, 'Max y', maxy)

    # minimum distance between squares
    min_distance = squaresize + 20

    # Loop through the amount of squares and generate random startpoints for the squares
    while len(squarestartpoints) < amount_of_squares:
        squarestartpointx = random.randrange(
            x, maxx)
        squarestartpointy = random.randrange(
            y, maxy)

        # if the list is empty, append the first square
        if len(squarestartpoints) == 0:
            squarestartpoints.append((squarestartpointx, squarestartpointy))
        else:
            # if the list is not empty, check if the new square is far enough away from the existing squares
            is_far_enough = True
            for square in squarestartpoints:
                # Calculate the distance between the new square and the existing square
                distance_x = abs(square[0] - squarestartpointx)
                distance_y = abs(square[1] - squarestartpointy)
                distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
                if distance < min_distance:
                    is_far_enough = False
                    break

            # if the new square is far enough away from all existing squares, append it to the list
            if is_far_enough:
                squarestartpoints.append(
                    (squarestartpointx, squarestartpointy))

    return squarestartpoints


def drawSquares():
    # Select square tool
    selectSquareTool()
    # Locate canvas
    canvaslocation = locateCanvas()

    # Get square startpoints
    squarestartpoints = generateSquares(canvaslocation)
    print(squarestartpoints)
    for i in squarestartpoints:
        pyautogui.moveTo(i[0], i[1], duration=0.1)
        pyautogui.dragTo(i[0]+squaresize, i[1]+squaresize, button='left')

    # MOVE CURSOR OUT OF CANVAS AND CLICK SO LATEST SQUARE IS DESELECTED (selection gives it a different look)
    pyautogui.moveTo(canvaslocation[0] + canvaslocation[2],
                     canvaslocation[1]+canvaslocation[3], duration=0.1)
    pyautogui.click()
    locateAndCountSquares(canvaslocation)


def locateAndCountSquares(canvaslocation):
    # Locate squares, count them, and print the total number
    squares = pyautogui.locateAllOnScreen('square.png')
    totalnumber = sum(1 for square in squares)
    if totalnumber > 0:
        # if squares found, mess up the canvas
        print('TOTAL NUMBER OF SQUARES IS', totalnumber)
        messUpTheCanvas(canvaslocation)
    else:
        # if no squares found, close paint
        print('NO SQUARES FOUND, GREAT SUCCESS!')
        pyautogui.hotkey('alt', 'f4')
        pyautogui.press('right')
        pyautogui.press('enter')


def messUpTheCanvas(canvaslocation):
    # Get the canvas in the same way we got the squares
    safetymargins = 10
    x, y = canvaslocation[0], canvaslocation[1]
    maxx = canvaslocation[2] - squaresize - safetymargins
    maxy = canvaslocation[3]

    # Select pencil tool
    selectBrushTool()

    # Move to the top-left corner of the canvas
    pyautogui.moveTo(x + safetymargins, y + safetymargins)

    # Draw lines from left to right, covering the whole screen
    for i in range(safetymargins, maxy, 50):
        pyautogui.dragTo(maxx + safetymargins, y + i, button='left')
        pyautogui.moveTo(x + safetymargins, y + i + 50)

    # Move the cursor back to the top-left corner of the canvas
    pyautogui.moveTo(x + safetymargins, y + safetymargins)

    # Return to counting the squares
    locateAndCountSquares(canvaslocation)


# Start the program, use either openMSPaint() or openMSPaintWithImageRecognition()
# openMSPaintWithImageRecognition()
openMSPaint()
