import pygame
import numpy as np


from multiprocessing import Process, Value
from copy import deepcopy
from defaults import Defaults
from grid import Grid
from drawUtil import DrawUtil
from camera import Camera





def runGameOfLife(matrix : [[]], boundaryCondition : str, musicName : str) -> bool:
    """
    Main function to start the Simulation Mode

    Args: 

     - matrix: Matrix to initialize the board with
    Return:
     - No return Statements    
    """

    pygame.init()
    #pygame.mixer.init()
    #pygame.mixer.music.load(os.path.join(os.getcwd(), "music", musicName + ".mp3"))
    #pygame.mixer.music.play()

    # Set the width and height of the screen [width, height]
    size = (Defaults.wWidth, Defaults.wHeight)
    screen = pygame.display.set_mode(size)
    screen.set_alpha(None)

    pygame.display.set_caption(Defaults.title)

    # Loop until the user clicks the close button.
    done, handled = False, False

    #is the player Moving
    isMoving = False
    #the mouse position when the player started moving 
    relMousePos = (0, 0)

    #if the simulation is running
    isRunning = False

    #simulation speed
    simulationSpeed = Defaults.simulationSpeed
    speedSteps = Defaults.speedSteps
    #passed time
    passedTime = 0

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    #instantiate grid and camera
    global grid
    grid, camera = Grid(matrix, boundaryCondition), Camera(Defaults.wWidth, Defaults.wHeight)



    
    # -------- Main Program Loop -----------
    while not done:
        # --- Main event loop (HANDLE USER INPUT)
        for event in pygame.event.get():
            #check if wheel is scrolled
            if event.type == pygame.MOUSEBUTTONDOWN:
                #zoom out
                if event.button == 4:
                    camera.zoomOut()
                    grid.fullRedraw()
                #zoom in
                if event.button == 5:
                    camera.zoomIn()
                    grid.fullRedraw()
            if event.type == pygame.QUIT:
                done = True
    

        # --- Game logic should go here

        #HANDLE USER INPUT
        #MOVING THE BOARD
        #print("camera position:", relMousePos[0] - pygame.mouse.get_pos()[0], relMousePos[1] - pygame.mouse.get_pos()[1])
        if pygame.mouse.get_pressed()[0] == True and pygame.mouse.get_pressed()[2] == True and isMoving == False:
            relMousePos = pygame.mouse.get_pos()
            isMoving = True
        if pygame.mouse.get_pressed()[0] == False or pygame.mouse.get_pressed()[2] == False:
            isMoving = False
        if isMoving:
            newCamPos = (pygame.mouse.get_pos()[0] - relMousePos[0],
                        pygame.mouse.get_pos()[1] - relMousePos[1])
            camera.setPos(newCamPos)
            grid.fullRedraw()
        
        #INITIALIZE BOARD
        if(grid.currentTime == 0):
            # check that the cursor is not out of range
            # the absolute position of the mouse needs to be shifted by the amount the grid was moved
            currentRelativeMouseX = pygame.mouse.get_pos()[0] - camera.pos[0]
            currentRelativeMouseY = pygame.mouse.get_pos()[1] - camera.pos[1]
            # the position also needs to be shifted by the zoom factor (zoomed in/out)
            relCellHeight = Defaults.cellHeight + camera.currentZoom
            relCellWidth = Defaults.cellWidth + camera.currentZoom
            # the current position needs to be in the grid-bounds
            if(0 <= currentRelativeMouseX // relCellWidth < grid.currentSizeX and \
            0 <= currentRelativeMouseY // relCellHeight < grid.currentSizeY):
                #add alive cell(s) (if the left mouse button was clicked)
                if(pygame.mouse.get_pressed()[0] == True and pygame.mouse.get_pressed()[1] == False):
                        grid.grid[currentRelativeMouseX // relCellHeight] \
                                [currentRelativeMouseY // relCellWidth] = 1
                        x = currentRelativeMouseX // relCellWidth
                        y = currentRelativeMouseY // relCellHeight
                        grid.cellsToUpdate.append((x, y))
                #remove alive cell(s) (if the right mouse button was clicked)
                if(pygame.mouse.get_pressed()[2] == True and pygame.mouse.get_pressed()[0] == False):
                        grid.grid[currentRelativeMouseX // relCellHeight] \
                                [currentRelativeMouseY // relCellWidth] = 0
                        x = currentRelativeMouseX // relCellWidth
                        y = currentRelativeMouseY // relCellHeight
                        grid.cellsToUpdate.append((x, y))

        #MENUBAR CONTROL
        if(pygame.mouse.get_pressed()[0] == True):
            if(handled == False):
                #play/pause-button check y-pos and x-pos
                if(Defaults.stButtonPos[1] <=
                pygame.mouse.get_pos()[1] <=
                Defaults.stButtonPos[1] + Defaults.stButtonSize and
                Defaults.stButtonPos[0] <=
                pygame.mouse.get_pos()[0] <=
                Defaults.stButtonPos[0] + Defaults.stButtonSize):
                    isRunning = not isRunning
                #one-step-button
                if(Defaults.oneStepButtonPos[1] <=
                pygame.mouse.get_pos()[1] <=
                Defaults.oneStepButtonPos[1] + Defaults.oneStepButtonSize and
                Defaults.oneStepButtonPos[0] <=
                pygame.mouse.get_pos()[0] <=
                Defaults.oneStepButtonPos[0] + Defaults.oneStepButtonSize):
                    if(isRunning == False):
                        grid.applyRules()
            #speed-up-button
            if(Defaults.spUpButtonPos[1] <=
            pygame.mouse.get_pos()[1] <=
            Defaults.spUpButtonPos[1] + Defaults.spUpButtonSize and
            Defaults.spUpButtonPos[0] <=
            pygame.mouse.get_pos()[0] <=
            Defaults.spUpButtonPos[0] + Defaults.spUpButtonSize):
                
                if(simulationSpeed - speedSteps > 0):
                    simulationSpeed -= speedSteps
            #speed-down-button
            if(Defaults.spDownButtonPos[1] <=
            pygame.mouse.get_pos()[1] <=
            Defaults.spDownButtonPos[1] + Defaults.spDownButtonSize and
            Defaults.spDownButtonPos[0] <=
            pygame.mouse.get_pos()[0] <=
            Defaults.spDownButtonPos[0] + Defaults.spDownButtonSize):
                simulationSpeed += speedSteps
            #back-to-menu-button
            if(Defaults.menuButtonPos[1] <=
               pygame.mouse.get_pos()[1] <=
               Defaults.menuButtonPos[1] + Defaults.menuButtonSize and
               Defaults.menuButtonPos[0] <=
               pygame.mouse.get_pos()[0] <=
               Defaults.menuButtonPos[0] + Defaults.menuButtonSize):
                pygame.display.quit()
                return 1
        #set handled
        if(pygame.mouse.get_pressed()[0] == True and not handled):
            handled = True
        if(pygame.mouse.get_pressed()[0] == False):
            handled = False

        #update the game accordingly to the set speed
        if(isRunning):
            if(simulationSpeed - passedTime <= 0):

                #COMPUTE NEW ITERATION 
                #copy current state
                futureGrid = deepcopy(grid.grid)


                v = Value('grid', np.zeros((200, 200)))
                procs = [Process(target=processCell, args=(cX, v)) for cX in range(grid.currentSizeX)]

                for p in procs: p.start()
                for p in procs: p.join()

                #iterate ove all cells
                #futureGrid = Parallel(n_jobs=-1, prefer='processes')(delayed(processCell)(cX) for cX in range(grid.currentSizeX))
                
                #copy the new grid to the old and increase the time
                grid.grid = np.array(futureGrid)
                grid.currentTime += 1

                passedTime = 0

        # --- Drawing code should go here
        if(grid.fullRedrawRequired):
            #Clear the screen
            screen.fill(Defaults.WHITE)
            #print(camera.pos)
            pygame.draw.rect(screen, Defaults.WHITE,
                        pygame.Rect(
                            camera.pos[0],
                            camera.pos[1],
                            (Defaults.cellHeight * grid.currentSizeX + (camera.currentZoom * grid.currentSizeX)),
                            (Defaults.cellWidth * grid.currentSizeY + (camera.currentZoom * grid.currentSizeY))))
            grid.fullRedrawRequired = False
        #Draw the grid
        if(grid.redrawRequired):
            for cell in grid.cellsToUpdate:
                #draw dead cells
                if grid.grid[cell[0]][cell[1]] == 0:
                    screen.fill(Defaults.BLACK,
                                pygame.Rect(
                                    (cell[0] * (Defaults.cellHeight + camera.currentZoom) + camera.pos[0]) + 1,
                                    (cell[1] * (Defaults.cellWidth + camera.currentZoom) + camera.pos[1]) + 1,
                                    ((Defaults.cellHeight + camera.currentZoom) - 2),
                                    ((Defaults.cellWidth + camera.currentZoom) - 2)))
                #draw alive cells
                else:
                    screen.fill(Defaults.WHITE,
                                pygame.Rect(
                                    cell[0] * (Defaults.cellHeight + camera.currentZoom) + camera.pos[0],
                                    cell[1] * (Defaults.cellWidth + camera.currentZoom) + camera.pos[1],
                                    Defaults.cellHeight + camera.currentZoom,
                                    Defaults.cellWidth + camera.currentZoom))
            grid.cellsToUpdate = []

        #draw a white rect for the menubar (draw over the grid if it is moved)
        DrawUtil.drawRectWithBorder(screen, Defaults.BLACK, Defaults.WHITE, 0, Defaults.gridSize,
                                    Defaults.gridSize, Defaults.menubarHeight, 2)
        #Draw play/stop-button
        DrawUtil.drawRectWithBorder(screen, Defaults.BLACK, Defaults.WHITE, Defaults.stButtonPos[0], Defaults.stButtonPos[1],
                                            Defaults.stButtonSize, Defaults.stButtonSize, 2)
        #draw pause-square
        if(isRunning):
            pygame.draw.rect(screen, Defaults.BLACK, ((Defaults.stButtonPos[0] + 10, Defaults.stButtonPos[1] + 10), (20, 20)))
        #draw running-arrow
        else:
            pygame.draw.polygon(screen, Defaults.BLACK, Defaults.stButtonTrianglePoints)
        #Draw speed-up-button
        DrawUtil.drawRectWithBorder(screen, Defaults.BLACK, Defaults.WHITE, Defaults.spUpButtonPos[0], Defaults.spUpButtonPos[1],
                                    Defaults.spUpButtonSize, Defaults.spUpButtonSize, 2)
        DrawUtil.drawRectWithBorder(screen, Defaults.BLACK, Defaults.BLACK, Defaults.spUpButtonPos[0] + 15, Defaults.spUpButtonPos[1] + 5,
                                    10, 30, 2)
        DrawUtil.drawRectWithBorder(screen, Defaults.BLACK, Defaults.BLACK, Defaults.spUpButtonPos[0] + 5, Defaults.spUpButtonPos[1] + 15,
                                    30, 10, 2)
        #Draw speed-down-button
        DrawUtil.drawRectWithBorder(screen, Defaults.BLACK, Defaults.WHITE, Defaults.spDownButtonPos[0], Defaults.spDownButtonPos[1],
                                    Defaults.spUpButtonSize, Defaults.spUpButtonSize, 2)
        DrawUtil.drawRectWithBorder(screen, Defaults.BLACK, Defaults.BLACK, Defaults.spDownButtonPos[0] + 5, Defaults.spDownButtonPos[1] + 15,
                                    30, 10, 2)
        #draw the one-step-button
        DrawUtil.drawRectWithBorder(screen, Defaults.BLACK, Defaults.WHITE, Defaults.oneStepButtonPos[0], Defaults.oneStepButtonPos[1],
                                    Defaults.oneStepButtonSize, Defaults.oneStepButtonSize, 2)
        pygame.draw.rect(screen, Defaults.BLACK, ((Defaults.oneStepButtonPos[0] + 10, Defaults.oneStepButtonPos[1] + 15), (10, 10)))
        pygame.draw.polygon(screen, Defaults.BLACK, Defaults.oneStepButtonTrianglePoints)


        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
    

        # --- Limit to 60 frames per second
        clock.tick(0)

        #increase the passed time
        passedTime += 1
 
    # Close the window and quit.
    pygame.quit()

def processCell(cX, grid) -> (int):
    """
    Apply the rules to all cells.
    """


    newRow = np.zeros((grid.currentSizeX))

    for cY in range(0, grid.currentSizeY):
        #the value of the new cell
        currentCell, newCell = grid.grid[cX][cY], grid.grid[cX][cY]

        #check if this cell is near the border
        _left, _top, _right, _bottom = False, False, False, False

        neighbors = boundaryCondition(cX, cY, grid) - newCell

        #apply the rules
        if(currentCell == 0):
            if(neighbors == 3):
                newCell = 1

        if(currentCell == 1):
            if(neighbors < 2):
                newCell = 0
            if(neighbors == 2 or neighbors == 3):
                newCell = 1
            if(neighbors > 3):
                newCell = 0

        if(newCell == 1):
            if(cY <= 2):
                _top = True
            if(cY >= grid.currentSizeY - 2):
                _bottom = True
            if(cX <= 2):
                _left = True
            if(cX >= grid.currentSizeX - 2):
                _right = True

        #redraw a cell if its state has changed
        #and a full redraw is not necessary 
        if newCell != grid.grid[cX][cY] and \
            not grid.fullRedrawRequired:
            grid.redrawRequired = True
            grid.cellsToUpdate.append((cX, cY))

        newRow[cY] = newCell

    return newRow#, _left, _top, _right, _bottom

def boundaryCondition(cX : int, cY : int):
    """
    Calculate the next cell value with the corresponding boundary condition.

    Args:
        cX : the x-position of the cell
        cY : the y-position of the cell

    Returns:
        the value of all neighbors
    """


    ret = 0

    if(Defaults.boundaryCondition == "absorbing"):
        lMarginX, lMarginY, rMarginX, rMarginY = 1, 1, 2, 2
        if(cX == 0):
            lMarginX = 0
        if(cY == 0):
            lMarginY = 0
        if(cX == grid.currentSizeX):
            rMarginX = 1
        if(cY == grid.currentSizeY):
            rMarginY = 1

        ret = grid.grid[cX - lMarginX : cX + rMarginX, cY - lMarginY : cY + rMarginY].sum()

    elif(Defaults.boundaryCondition == "periodic"):
        for x in range(cX - 1,cX + 2):
            tmpX = x
        if(x > grid.currentSizeX):
            tmpX = x - grid.currentSizeX
        if(x < 0):
            tmpX = x + grid.currentSizeX
            for y in range(cY - 1,cY + 2):
                tmpY = y
                if(y > grid.currentSizeY):
                    tmpY = y - grid.currentSizeY
                if(y < 0):
                    tmpY = y + grid.currentSizeY

                ret += grid.grid[tmpX][tmpY]
    #reflecting
    else:
        pass


    return ret

if __name__ == "__main__":
    runGameOfLife(np.zeros((200, 200)), "", "")
