import pygame
import numpy as np
import os

from defaults import Defaults
from grid import Grid
from drawUtil import DrawUtil
from camera import Camera
import IO


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
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
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

            if event.type == pygame.VIDEORESIZE:
                size = (event.w, event.h)
                print(event.w, event.h)
                screen = pygame.display.set_mode(size, pygame.RESIZABLE)
                grid.fullRedraw()
    

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

        #Difference between original window size and actual window size
        resizeValueX = (size[0] - Defaults.wWidth)/2
        resizeValueY = (size[1] - Defaults.wHeight)


        
        #Button positions relative to window size
        stButtonPos = list(Defaults.stButtonPos)
        stButtonPos[1] += resizeValueY
        stButtonPos[0] += resizeValueX

        oneStepButtonPos = list(Defaults.oneStepButtonPos)
        oneStepButtonPos[1] += resizeValueY
        oneStepButtonPos[0] += resizeValueX

        spUpButtonPos = list(Defaults.spUpButtonPos)
        spUpButtonPos[1] += resizeValueY
        spUpButtonPos[0] += resizeValueX

        spDownButtonPos = list(Defaults.spDownButtonPos)
        spDownButtonPos[1] += resizeValueY
        spDownButtonPos[0] += resizeValueX

        menuButtonPos = list(Defaults.menuButtonPos)
        menuButtonPos[1] += resizeValueY
        menuButtonPos[0] += resizeValueX

        saveGridButtonPos = list(Defaults.saveGridButtonPos)
        saveGridButtonPos[1] += resizeValueY
        saveGridButtonPos[0] += resizeValueX




        #MENUBAR CONTROL
        if(pygame.mouse.get_pressed()[0] == True):
            if(handled == False):
                #play/pause-button check y-pos and x-pos
                if(stButtonPos[1] <=
                pygame.mouse.get_pos()[1] <=
                stButtonPos[1] + Defaults.stButtonSize and
                stButtonPos[0] <=
                pygame.mouse.get_pos()[0] <=
                stButtonPos[0] + Defaults.stButtonSize):
                    isRunning = not isRunning
                #one-step-button
                if(oneStepButtonPos[1] <=
                pygame.mouse.get_pos()[1] <=
                oneStepButtonPos[1] + Defaults.oneStepButtonSize and
                oneStepButtonPos[0] <=
                pygame.mouse.get_pos()[0] <=
                oneStepButtonPos[0] + Defaults.oneStepButtonSize):
                    if(isRunning == False):
                        grid.applyRules()
            #speed-up-button
            if(spUpButtonPos[1] <=
            pygame.mouse.get_pos()[1] <=
            spUpButtonPos[1] + Defaults.spUpButtonSize and
            spUpButtonPos[0] <=
            pygame.mouse.get_pos()[0] <=
            spUpButtonPos[0] + Defaults.spUpButtonSize):
                
                if(simulationSpeed - speedSteps > 0):
                    simulationSpeed -= speedSteps
            #speed-down-button
            if(spDownButtonPos[1] <=
            pygame.mouse.get_pos()[1] <=
            spDownButtonPos[1] + Defaults.spDownButtonSize and
            spDownButtonPos[0] <=
            pygame.mouse.get_pos()[0] <=
            spDownButtonPos[0] + Defaults.spDownButtonSize):
                simulationSpeed += speedSteps
            #back-to-menu-button
            if(menuButtonPos[1] <=
               pygame.mouse.get_pos()[1] <=
               menuButtonPos[1] + Defaults.menuButtonSize and
               menuButtonPos[0] <=
               pygame.mouse.get_pos()[0] <=
               menuButtonPos[0] + Defaults.menuButtonSize):
                pygame.display.quit()
                return 1
            #save-grid-button
            if(saveGridButtonPos[1] <=
               pygame.mouse.get_pos()[1] <=
               saveGridButtonPos[1] + Defaults.saveGridButtonSize and
               saveGridButtonPos[0] <=
               pygame.mouse.get_pos()[0] <=
               saveGridButtonPos[0] + Defaults.saveGridButtonSize):  
                    
                    IO.saveGridWithFileBrowser(grid)
                    

                    
        #set handled
        if(pygame.mouse.get_pressed()[0] == True and not handled):
            handled = True
        if(pygame.mouse.get_pressed()[0] == False):
            handled = False

        #update the game accordingly to the set speed
        if(isRunning):
            if(simulationSpeed - passedTime <= 0):
                grid.applyRules()
                passedTime = 0

        # --- Drawing code should go here

        #FULL REDRAW
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


        
       
        #Draw play/stop-button
        DrawUtil.drawRectWithBorder(screen, Defaults.BLACK, Defaults.WHITE, stButtonPos[0], stButtonPos[1],
                                            Defaults.stButtonSize, Defaults.stButtonSize, 2)
        #draw pause-square
        if(isRunning):
            pygame.draw.rect(screen, Defaults.BLACK, ((stButtonPos[0] + 10, stButtonPos[1]+ 10), (20, 20)))
        #draw running-arrow
        else:
            stButtonTrianglePoints = [(stButtonPos[0] + 10, stButtonPos[1] + 10),
                                      (stButtonPos[0] + 30, stButtonPos[1] + 20),
                                      (stButtonPos[0] + 10, stButtonPos[1] + 30)]
            pygame.draw.polygon(screen, Defaults.BLACK, stButtonTrianglePoints)
        #Draw speed-up-button
        DrawUtil.drawRectWithBorder(screen, Defaults.BLACK, Defaults.WHITE, spUpButtonPos[0], spUpButtonPos[1],
                                    Defaults.spUpButtonSize, Defaults.spUpButtonSize, 2)
        DrawUtil.drawRectWithBorder(screen, Defaults.BLACK, Defaults.BLACK, spUpButtonPos[0] + 15, spUpButtonPos[1]+ 5,
                                    10, 30, 2)
        DrawUtil.drawRectWithBorder(screen, Defaults.BLACK, Defaults.BLACK, spUpButtonPos[0] + 5, spUpButtonPos[1]+ 15,
                                    30, 10, 2)
        #Draw speed-down-button
        DrawUtil.drawRectWithBorder(screen, Defaults.BLACK, Defaults.WHITE, spDownButtonPos[0], spDownButtonPos[1],
                                    Defaults.spUpButtonSize, Defaults.spUpButtonSize, 2)
        DrawUtil.drawRectWithBorder(screen, Defaults.BLACK, Defaults.BLACK, spDownButtonPos[0] + 5, spDownButtonPos[1] + 15,
                                    30, 10, 2)
        #draw the one-step-button
        DrawUtil.drawRectWithBorder(screen, Defaults.BLACK, Defaults.WHITE, oneStepButtonPos[0], oneStepButtonPos[1],
                                    Defaults.oneStepButtonSize, Defaults.oneStepButtonSize, 2)
        pygame.draw.rect(screen, Defaults.BLACK, ((oneStepButtonPos[0] + 10, oneStepButtonPos[1] + 15), (10, 10)))
        oneStepButtonTrianglePoints = [(oneStepButtonPos[0] + 20, oneStepButtonPos[1] + 10),
                                      (oneStepButtonPos[0] + 30, oneStepButtonPos[1] + 20),
                                      (oneStepButtonPos[0] + 20, oneStepButtonPos[1] + 30)]
        pygame.draw.polygon(screen, Defaults.BLACK, oneStepButtonTrianglePoints)
        #Draw save-grid-button
        DrawUtil.drawRectWithBorder(screen, Defaults.BLACK, Defaults.WHITE, saveGridButtonPos[0], saveGridButtonPos[1],
                                           Defaults.saveGridButtonSize, Defaults.saveGridButtonSize, 2)
        myfont = pygame.font.SysFont('Sans Bold', 17)
        textsurface = myfont.render('SAVE', False, (0, 0, 0))
        screen.blit(textsurface,(saveGridButtonPos[0]+5,saveGridButtonPos[1]+15))

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
    

        # --- Limit to 60 frames per second
        clock.tick(0)

        #increase the passed time
        passedTime += 1
 
    # Close the window and quit.
    pygame.quit()

if __name__ == "__main__":
    testArr = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    runGameOfLife(np.zeros((15, 15)), "periodic", "miniboss")
