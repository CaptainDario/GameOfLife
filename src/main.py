import pygame
import math

from defaults import Defaults
from grid import Grid
from drawUtil import DrawUtil
from camera import Camera


pygame.init()
 
# Set the width and height of the screen [width, height]
size = (Defaults.wHeight, Defaults.wWidth)
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
simulationSpeed = 15
speedSteps = 1
#passed time
passedTime = 0

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

#instantiate grid and camera
grid, camera = Grid(), Camera(Defaults.wWidth, Defaults.wHeight)



 
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
        currentRelativeMouseX = pygame.mouse.get_pos()[1] - camera.pos[1]
        currentRelativeMouseY = pygame.mouse.get_pos()[0] - camera.pos[0]
        # the position also needs to be shifted by the zoom factor (zoomed in/out)
        relCellHeight = Defaults.cellHeight + camera.currentZoom
        relCellWidth = Defaults.cellWidth + camera.currentZoom
        # the current position needs to be in the grid-bounds
        if(0 <= currentRelativeMouseX // relCellWidth < grid.currentSize and \
           0 <= currentRelativeMouseY // relCellHeight < grid.currentSize):
            #add alive cell(s) (if the left mouse button was clicked)
            if(pygame.mouse.get_pressed()[0] == True and pygame.mouse.get_pressed()[1] == False):
                    grid.grid[currentRelativeMouseY // relCellHeight] \
                            [currentRelativeMouseX // relCellWidth] = 1
                    grid.cellsToUpdate[currentRelativeMouseY // relCellHeight * grid.currentSize + currentRelativeMouseX // relCellWidth] = 1
            #remove alive cell(s) (if the right mouse button was clicked)
            if(pygame.mouse.get_pressed()[2] == True and pygame.mouse.get_pressed()[0] == False):
                    grid.grid[currentRelativeMouseY // relCellHeight] \
                            [currentRelativeMouseX // relCellWidth] = 0
                    grid.cellsToUpdate[currentRelativeMouseY // relCellHeight * grid.currentSize + currentRelativeMouseX // relCellWidth] = 1

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
    if(grid.fullRedrawRequired):
        #Clear the screen
        screen.fill(Defaults.BLACK)
        #print(camera.pos)
        pygame.draw.rect(screen, Defaults.WHITE,
                    pygame.Rect(
                        camera.pos[0],
                        camera.pos[1],
                        (Defaults.cellHeight * grid.currentSize + (camera.currentZoom * grid.currentSize)),
                        (Defaults.cellWidth * grid.currentSize + (camera.currentZoom * grid.currentSize))))
        grid.fullRedrawRequired = False
    #Draw the grid
    if(grid.redrawRequired):
        for c, item in enumerate(grid.cellsToUpdate):
            cell = (math.floor(c / grid.currentSize), c % grid.currentSize)
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
            grid.cellsToUpdate[c] = 0

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