import pyautogui
import random
from toolselectors import selectBrushTool, selectSquareTool, selectTypeTool
from canvasruiners  import draw_number_on_canvas, write_number_on_square, mess_up_the_canvas

# Activate failsafe to interrupt if needed
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5
# Init these for pyautogui
screenwidth, screenheight = pyautogui.size()
# Method to use to mess up the canvas, change to 1, 2 or 3 if you don't want user input
method = input('\n\tSelect method to mess up the canvas (1=write_number_on_square, 2=draw_number_on_square, 3=mess_up_the_canvas): \n\n\t')
# In case user doesn't enter a valid method, keep asking until they do
while method != '1' and method != '2' and method != '3':
    method = input('\tPlease select a valid method (1, 2 or 3): \n\n\t')
# Determine if you want to use notepad for communication, change to False if you want to use the console exclusively
notedpad_enabled = True
# Squaresize for squares.. change this if you want larger or smaller ones
squaresize = 150

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
        location = pyautogui.locateOnScreen(
            'referenceimages/paint.png', confidence=0.8)
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
    location = pyautogui.locateOnScreen(
        'referenceimages/canvas.png', confidence=0.8)
    return location


def drawSquares():
    # locate canvas
    canvaslocation = locateCanvas()
    # maximize window if not maximized
    pyautogui.hotkey('wind', 'up')
    # Select square tool
    selectSquareTool()

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
            pyautogui.moveTo(
                canvaslocation[0] + canvaslocation[2], canvaslocation[3]//2)
            pyautogui.click()
            screenshot = pyautogui.screenshot(
                region=(i[0], i[1], squaresize, squaresize))
            screenshot.save('referenceimages/screenshot_of_square.png')

    # MOVE CURSOR OUT OF CANVAS AND CLICK SO LATEST SQUARE IS DESELECTED (selection gives it a different look)
    pyautogui.moveTo(canvaslocation[0] +
                     canvaslocation[2], canvaslocation[3]//2)
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
    maxx = canvaslocation[2] - safetymargins - squaresize
    maxy = canvaslocation[3] - safetymargins - squaresize
    # Console logs for debugging
    print('Number of squares:', amount_of_squares)
    print('Canvas specs', canvaslocation)
    print('Screen specs', screenwidth, screenheight)
    print('Max x', maxx, 'Max y', maxy)
    print('x', x, 'y', y)

    # minimum distance between squares (10 px)
    min_distance = squaresize + 10

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
    print('Generated squares: ', squarestartpoints)
    return squarestartpoints


def locateAndCountSquares(canvaslocation):
    # Locate squares, count them, and print the total number
    squares = list(pyautogui.locateAllOnScreen(
        'referenceimages/screenshot_of_square.png'))
    totalnumber = len(squares)

    # if squares found, draw on squares and count them again
    if totalnumber > 0:
        print('\n\nTOTAL NUMBER OF SQUARES DETECTED: ', totalnumber)
        # Loop thorugh all the squares and type the number on them
        if method == str(1):
            selectTypeTool()
            for index, squarelocation in enumerate(squares):
                write_number_on_square(index+1, squarelocation, squaresize)
            locateAndCountSquares(canvaslocation)
        # Loop through all the found squares and draw numbers on them
        if method == str(2):
            selectBrushTool()
            for index, squarelocation in enumerate(squares):
                draw_number_on_canvas(
                    index+1, [squarelocation[0], squarelocation[1]], squaresize)
            locateAndCountSquares(canvaslocation)
        # Mess up the canvas and count the squares again
        if method == str(3):
            if notedpad_enabled: openNotePadAndType('TOTAL NUMBER OF SQUARES DETECTED: ' + str(totalnumber))   
            mess_up_the_canvas(canvaslocation, squaresize)
            locateAndCountSquares(canvaslocation)

    else:
        # if no squares found, close paint
        if notedpad_enabled: openNotePadAndType(
            'NO SQUARES FOUND AFTER DRAWING/TYPING ON THEM, CLOSING PAINT')
        print('NO SQUARES FOUND AFTER DRAWING/TYPING ON THEM, CLOSING PAINT\n\n')
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
