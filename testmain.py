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

def draw_number_on_canvas(number, squarelocation):
    
    # define the numbers as a list of coordinates
    numbers_to_draw = [
    ((100, 100), (200, 100), (200, 200), (100, 200), (100, 100)),  # 0
    ((150, 100), (150, 200)),  # 1
    ((100, 100), (200, 100), (200, 150), (100, 150), (100, 200), (200, 200)),  # 2
    ((100, 100), (200, 100), (200, 150), (100, 150) , (200, 150), (200, 200), (100, 200)) ,  # 3
    ((100, 100), (100, 150), (200, 150), (200, 100), (200, 200)),  # 4
    ((200, 100), (100, 100), (100, 150), (200, 150), (200, 200), (100, 200)),  # 5
]

    # move the mouse to the starting position of the number
    pyautogui.moveTo(squarelocation[0] + numbers_to_draw[number][0][0] - squaresize//2,
                      squarelocation[1] + numbers_to_draw[number][0][1] - squaresize//2)

    # click and drag the mouse to draw the number
    pyautogui.mouseDown()
    # loop through the coordinates and draw the number
    for point in numbers_to_draw[number][1:]:
        pyautogui.moveTo(squarelocation[0]- squaresize//2 + point[0], squarelocation[1]- squaresize//2 + point[1])
        time.sleep(0.05)
    pyautogui.mouseUp()


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

    locateAndCountSquares(canvaslocation, squarestartpoints)


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


def locateAndCountSquares(canvaslocation, squarestartpoints=[]):
    # Locate squares, count them, and print the total number
    squares = pyautogui.locateAllOnScreen('referenceimages/screenshot_of_square.png')
    totalnumber = sum(1 for square in squares)

    if totalnumber > 0:
        # if squares found, draw on squares and count them again
        openNotePadAndType('TOTAL NUMBER OF SQUARES DETECTED: ' + str(totalnumber)) 
        print('\n\nTOTAL NUMBER OF SQUARES DETECTED: ', totalnumber)
        if squarestartpoints:
            selectBrushTool()
            for index, squarelocation in enumerate(squarestartpoints):
                draw_number_on_canvas(index+1, squarelocation)
        locateAndCountSquares(canvaslocation)
    else:
        # if no squares found, close paint
        openNotePadAndType('NO SQUARES FOUND AFTER DRAWING ON SQUARES, CLOSING PAINT')   
        print('NO SQUARES FOUND AFTER MESSING UP THE CANVAS, CLOSING PAINT\n\n')
        pyautogui.hotkey('alt', 'f4')
        pyautogui.press('right')
        pyautogui.press('enter')    


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
