import pyautogui
import random
from toolselectors import selectBrushTool, selectSquareTool
import time
# Activate failsafe to interrupt if needed
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5
# Squaresize for squares.. change this if you want larger or smaller ones
squaresize = 150
# Init these for pyautogui
screenwidth, screenheight = pyautogui.size()


# Simplest strategy to open Paint
def openMSPaint():
    # Press windows key, type paint, and press enter
    pyautogui.press('win')
    pyautogui.typewrite('Paint', 0.1)
    pyautogui.press('enter')
    # maximize window if not maximized
    pyautogui.hotkey('win', 'up')
    drawSquares()

# Open Paint with image recognition
def openMSPaintWithImageRecognition():
    # Press windows key, type paint
    pyautogui.press('win')
    pyautogui.typewrite('Paint', 0.1)
    # Try to find the paint icon
    try:
        location = pyautogui.locateOnScreen('referenceimages/paint.png', confidence=0.8)
        # If the icon is found, set the mouse to the center of the icon and click
        x, y, wid, hei = location
        x += wid//2
        y += hei//2
        pyautogui.moveTo(x, y, duration=0.1)
        pyautogui.click()
    except:
        print('Could not find Paint icon')
    # maximize window if not maximized
    pyautogui.hotkey('win', 'up')
    drawSquares()


def locateCanvas():
    # Locate canvas
    location = pyautogui.locateOnScreen('referenceimages/canvas.png', confidence=0.8)
    return location


def drawSquares():
    # maximize window if not maximized
    pyautogui.hotkey('wind', 'up')
    # Select square tool
    selectSquareTool()
    # Locate canvas
    canvaslocation = locateCanvas()

    # Get square startpoints
    squarestartpoints = generateSquares(canvaslocation)
    # Loop through squares and draw them (take screenshot at first square for later reference)
    for index, i in enumerate(squarestartpoints):
        pyautogui.moveTo(i[0], i[1])
        pyautogui.dragTo(i[0]+squaresize, i[1]+squaresize, button='left')
        # If first square drawn, take screenshot and save for later reference. This screenshot will be used in the image recognition phase
        if index == 0:
            print('Index is 0, taking screenshot of square')
            # MOVE CURSOR OUT OF CANVAS AND CLICK SO LATEST SQUARE IS DESELECTED (selection gives it a different look)
            pyautogui.moveTo(canvaslocation[0] + canvaslocation[2], canvaslocation[3]//2)
            pyautogui.click()
            screenshot = pyautogui.screenshot(
                region=(i[0], i[1], squaresize, squaresize))
            screenshot.save('referenceimages/screenshot_of_square.png')

    # MOVE CURSOR OUT OF CANVAS AND CLICK SO LATEST SQUARE IS DESELECTED (selection gives it a different look)
    pyautogui.moveTo(canvaslocation[0] + canvaslocation[2], canvaslocation[3]//2)
    pyautogui.click()

    locateAndCountSquares(canvaslocation)


def generateSquares(canvaslocation):
    
    # Init list of existing squares. Also get the amount of squares (2-5)
    squarestartpoints = []
    amount_of_squares = random.randrange(2, 6)
    # Get the possible locations for the squares
    # Safetymargins are added to prevent the squares from being drawn right at the border of the canvas. This wont cause problems for image recognition but is done for aestethic reasons :D 
    safetymargins = 10
    x, y = canvaslocation[0] + safetymargins, canvaslocation[1] + safetymargins
    maxx = canvaslocation[2] -  safetymargins - squaresize
    maxy = canvaslocation[3] -  safetymargins - squaresize
    # Console logs for debugging
    print('Number of squares:', amount_of_squares)
    print('Canvas specs', canvaslocation)
    print('Screen specs', screenwidth, screenheight)
    print('Max x', maxx, 'Max y', maxy)
    print('x', x, 'y', y)

    # minimum distance between squares (10 px)
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
                if distance_x < min_distance and distance_y < min_distance:
                    is_far_enough = False
                    break

            # if the new square is far enough away from all existing squares, append it to the list
            if is_far_enough:
                squarestartpoints.append(
                    (squarestartpointx, squarestartpointy))
    print(squarestartpoints)
    return squarestartpoints


def locateAndCountSquares(canvaslocation):
    # Locate squares, count them, and print the total number
    squares = pyautogui.locateAllOnScreen('referenceimages/screenshot_of_square.png')
    totalnumber = sum(1 for square in squares)

    if totalnumber > 0:
        # if squares found, mess up the canvas
        openNotePadAndType('TOTAL NUMBER OF SQUARES DETECTED: ' + str(totalnumber))   
        print('\n\nTOTAL NUMBER OF SQUARES DETECTED: ', totalnumber)
        messUpTheCanvas(canvaslocation)
    else:
        # if no squares found, close paint
        openNotePadAndType('NO SQUARES FOUND AFTER MESSING UP THE CANVAS, CLOSING PAINT')   
        print('NO SQUARES FOUND AFTER MESSING UP THE CANVAS, CLOSING PAINT\n\n')
        pyautogui.hotkey('alt', 'f4')
        pyautogui.press('right')
        pyautogui.press('enter')    


def messUpTheCanvas(canvaslocation):
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

    # Return to counting the squares
    locateAndCountSquares(canvaslocation)

# Function to type messages to notepad
def openNotePadAndType(message):
    # Press windows key, type notepad, and press enter
    pyautogui.press('win')
    pyautogui.typewrite('Notepad', 0.1)
    pyautogui.press('enter')
    # Type message
    pyautogui.write(message, 0.1)
    # Close notepad
    pyautogui.hotkey('alt', 'f4')
    pyautogui.press('right')
    pyautogui.press('enter') 

# Start the program, use either openMSPaint() or openMSPaintWithImageRecognition()
# openMSPaintWithImageRecognition()
openMSPaint()
