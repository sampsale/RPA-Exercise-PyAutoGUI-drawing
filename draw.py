import pyautogui
from toolselectors import selectBrushTool, selectSquareTool
import random
import math
screenwidth, screenheight = pyautogui.size()


def generateSquares(canvaslocation, squaresize):
    
    # Init squaresize and list of existing squares. Also get the amount of squares (3-5)
    squarestartpoints = []
    amount_of_squares = random.randrange(3, 6)
    # Console logs for debugging
    print('Number of squares:', amount_of_squares)
    print('Canvas specs', canvaslocation)
    print('Screen specs', screenwidth, screenheight)

    safetymargins = 10
    # Get the possible locations for the squares
    # Safetymargins are added to prevent the squares from being drawn right at the border of the canvas
    x, y = canvaslocation[0], canvaslocation[1]
    maxx = canvaslocation[2] - squaresize*2 - safetymargins
    maxy = canvaslocation[3] - squaresize*2 - safetymargins

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
                squarestartpoints.append((squarestartpointx, squarestartpointy))

    return squarestartpoints


def drawSquares(squaresize, canvaslocation):
    # Select square tool
    selectSquareTool()
    # Locate canvas
    print('TEST', canvaslocation)

    # Get square startpoints
    squarestartpoints = generateSquares(canvaslocation, squaresize)
    print(squarestartpoints)
    for i in squarestartpoints:
        pyautogui.moveTo(i[0], i[1], duration=0.1)
        pyautogui.dragTo(i[0]+squaresize, i[1]+squaresize, button='left')
    
    # MOVE CURSOR OUT OF CANVAS AND CLICK SO LATEST SQUARE IS DESELECTED (selection gives it a different look)
    pyautogui.moveTo(canvaslocation[0] + canvaslocation[2], canvaslocation[1]+canvaslocation[3], duration=0.1)
    pyautogui.click()

def messUpTheCanvas(canvaslocation, squaresize):
    # Get the canvas in the same way we got the squares
    safetymargins = 10
    x, y = canvaslocation[0], canvaslocation[1]
    maxx = canvaslocation[2] - squaresize*2 - safetymargins
    maxy = canvaslocation[3] - squaresize*2 - safetymargins

    # Select pencil tool
    selectBrushTool()

    # Draw wavy lines
    while True:
        x1 = random.randint(x, maxx)
        y1 = random.randint(y, maxy)
        angle = random.uniform(0, math.pi*2)
        radius = random.uniform(20, 100)
        x2 = x1 + math.cos(angle) * radius
        y2 = y1 + math.sin(angle) * radius
        pyautogui.moveTo(x1, y1)
        pyautogui.dragTo(x2, y2, duration=0.05)