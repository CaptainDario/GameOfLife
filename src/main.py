import pygame

from defaults import Defaults
from grid import Grid
from drawUtil import DrawUtil


pygame.init()
 
# Set the width and height of the screen [width, height]
size = (Defaults.wHeight, Defaults.wWidth)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption(Defaults.title)
 
# Loop until the user clicks the close button.
done, handled = False, False
 
#if the simulation is running
isRunning = False

#simulation speed
simulationSpeed = 15
speedSteps = 1
#passed time
passedTime = 0

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

#instantiate grid
grid = Grid()

 
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        #check if wheel is scrolled
        if event.type == pygame.MOUSEBUTTONDOWN :
            #zoom in
            if event.button == 4:
                Defaults.cellHeight += 1
                Defaults.cellWidth += 1
            #zoom out
            if event.button == 5:
                Defaults.cellHeight -= 1
                Defaults.cellWidth -= 1
        if event.type == pygame.QUIT:
            done = True
 

    # --- Game logic should go here

    #HANDLE USER INPUT
    #INITIALIZE BOARD
    if(grid.currentTime == 0):
        #add alive cell
        if(pygame.mouse.get_pressed()[0] == True):
            if(pygame.mouse.get_pos()[1] < Defaults.gridSize):
                grid.grid[pygame.mouse.get_pos()[0] // Defaults.cellHeight]\
                        [pygame.mouse.get_pos()[1] // Defaults.cellWidth] = 1
        #remove alive cell
        if(pygame.mouse.get_pressed()[2] == True):
            if(pygame.mouse.get_pos()[1] < Defaults.gridSize):
                grid.grid[pygame.mouse.get_pos()[0] // Defaults.cellHeight]\
                        [pygame.mouse.get_pos()[1] // Defaults.cellWidth] = 0

    #MOUSE CONTROL
    #Do one simulation step when left clicked
    if(grid.currentTime > 0):
        #do one simulation step
        if(pygame.mouse.get_pressed()[0] == True and not handled):
            grid.applyRules()

    #update the game accordingly to the set spedd
    if(isRunning):
        if(simulationSpeed - passedTime <= 0):
            grid.applyRules()
            passedTime = 0


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


    # --- Screen-clearing code goes here
    screen.fill(Defaults.WHITE)
 

    # --- Drawing code should go here
    for cX, x in enumerate(grid.grid):
        for cY, y in enumerate(x):
            if not y:
                DrawUtil.drawRectWithBorder(screen, Defaults.BLACK, Defaults.WHITE, cX * Defaults.cellHeight, cY * Defaults.cellWidth,
                                            Defaults.cellHeight, Defaults.cellWidth, 1)
            else:
                DrawUtil.drawRectWithBorder(screen, Defaults.BLACK, Defaults.BLACK, cX * Defaults.cellHeight, cY * Defaults.cellWidth,
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
    
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 

    # --- Limit to 60 frames per second
    clock.tick(60)

    #increase the passed time
    passedTime += 1
 
# Close the window and quit.
pygame.quit()