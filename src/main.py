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
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

#instantiate grid
grid = Grid()

 
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 

    # --- Game logic should go here

    #USER INPUT
    #add alive cell
    if(pygame.mouse.get_pressed()[0] == True):
        grid.grid[pygame.mouse.get_pos()[0] // Defaults.cellHeight]\
                 [pygame.mouse.get_pos()[1] // Defaults.cellWidth] = 1
 
    #remove alive cell
    if(pygame.mouse.get_pressed()[2] == True):
        grid.grid[pygame.mouse.get_pos()[0] // Defaults.cellHeight]\
                 [pygame.mouse.get_pos()[1] // Defaults.cellWidth] = 0


    # --- Screen-clearing code goes here
    screen.fill(Defaults.WHITE)
 
    # --- Drawing code should go here
    for cX, x in enumerate(grid.grid):
        for cY, y in enumerate(x):
            if not y:
                DrawUtil.drawRectWithBorder(screen, Defaults.BLACK, Defaults.WHITE, cX * Defaults.cellHeight, cY * Defaults.cellWidth, Defaults.cellHeight, Defaults.cellWidth, 1)
            else:
                DrawUtil.drawRectWithBorder(screen, Defaults.BLACK, Defaults.BLACK, cX * Defaults.cellHeight, cY * Defaults.cellWidth, Defaults.cellHeight, Defaults.cellWidth, 1)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()