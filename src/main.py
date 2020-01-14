import pygame

from defaults import Defaults
from grid import Grid
from drawUtil import DrawUtil
from camera import Camera


pygame.init()
 
# Set the width and height of the screen [width, height]
size = (Defaults.wHeight, Defaults.wWidth)
screen = pygame.display.set_mode(size)
 
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
grid, camera = Grid(), Camera(Defaults.wWidth, Defaults.wHeight, Defaults.cellHeight)




 
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop (HANDLE USER INPUT)
    for event in pygame.event.get():
        #check if wheel is scrolled
        if event.type == pygame.MOUSEBUTTONDOWN:
            #zoom out
            if event.button == 4:
                #only until certain zoom factor
                if Defaults.cellHeight < camera.zoomOutLimit and \
                   Defaults.cellWidth < camera.zoomOutLimit:
                    Defaults.cellHeight += 1
                    Defaults.cellWidth += 1
            #zoom in
            if event.button == 5:
                #only if it is not to small
                if Defaults.cellHeight > camera.zoomInLimit and \
                   Defaults.cellWidth > camera.zoomInLimit:
                    Defaults.cellHeight -= 1
                    Defaults.cellWidth -= 1
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
    
    #INITIALIZE BOARD
    if(grid.currentTime == 0):
        #check that the cursor is not out of range
        if(0 <= pygame.mouse.get_pos()[1] - camera.pos[1] < Defaults.gridSize and \
           0 <= pygame.mouse.get_pos()[0] - camera.pos[0] < Defaults.gridSize):
            #add alive cell
            if(pygame.mouse.get_pressed()[0] == True and pygame.mouse.get_pressed()[1] == False):
                    grid.grid[(pygame.mouse.get_pos()[0] - camera.pos[0]) // Defaults.cellHeight] \
                            [(pygame.mouse.get_pos()[1] - camera.pos[1]) // Defaults.cellWidth] = 1
            #remove alive cell
            if(pygame.mouse.get_pressed()[2] == True and pygame.mouse.get_pressed()[0] == False):
                    grid.grid[(pygame.mouse.get_pos()[0] - camera.pos[0]) // Defaults.cellHeight]\
                            [(pygame.mouse.get_pos()[1] - camera.pos[1]) // Defaults.cellWidth] = 0

    #MENUBAR CONTROL
    if(pygame.mouse.get_pressed()[0] == True and handled == False):
        #play/pause-button check y-pos and x-pos
        if(Defaults.stButtonPos[1] <=
            pygame.mouse.get_pos()[1] <=
            Defaults.stButtonPos[1] + Defaults.stButtonSize and
            Defaults.stButtonPos[0] <=
            pygame.mouse.get_pos()[0] <=
            Defaults.stButtonPos[0] + Defaults.stButtonSize):
            isRunning = not isRunning
        #speed-up-button
        if(Defaults.spUpButtonPos[1] <=
            pygame.mouse.get_pos()[1] <=
            Defaults.spUpButtonPos[1] + Defaults.spUpButtonSize and
            Defaults.spUpButtonPos[0] <=
            pygame.mouse.get_pos()[0] <=
            Defaults.spUpButtonPos[0] + Defaults.spUpButtonSize):
            
            if(simulationSpeed - speedSteps > 0):
                print(simulationSpeed)
                simulationSpeed -= speedSteps
        #speed-down-button
        if(Defaults.spDownButtonPos[1] <=
            pygame.mouse.get_pos()[1] <=
            Defaults.spDownButtonPos[1] + Defaults.spDownButtonSize and
            Defaults.spDownButtonPos[0] <=
            pygame.mouse.get_pos()[0] <=
            Defaults.spDownButtonPos[0] + Defaults.spDownButtonSize):
            
            print(simulationSpeed)
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

    #Clear the screen
    screen.fill(Defaults.WHITE)
 

    # --- Drawing code should go here
    #Draw the grid
    for cX, x in enumerate(grid.grid):
        for cY, y in enumerate(x):
            if not y:
                DrawUtil.drawRectWithBorder(screen, Defaults.BLACK, Defaults.WHITE,
                                            cX * Defaults.cellHeight + camera.pos[0], cY * Defaults.cellWidth + camera.pos[1],
                                            Defaults.cellHeight, Defaults.cellWidth, 1)
            else:
                DrawUtil.drawRectWithBorder(screen, Defaults.BLACK, Defaults.BLACK,
                                            cX * Defaults.cellHeight + camera.pos[0], cY * Defaults.cellWidth + camera.pos[1],
                                            Defaults.cellHeight, Defaults.cellWidth, 1)
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
    pygame.draw.polygon(screen, Defaults.BLACK, Defaults.oneStepButtonTrianglePoints)


    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 

    # --- Limit to 60 frames per second
    clock.tick(60)

    #increase the passed time
    passedTime += 1
 
# Close the window and quit.
pygame.quit()