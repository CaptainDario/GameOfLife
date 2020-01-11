
class Defaults():
    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    #Game info
    name = "Game Of Life"
    version = "v0.0.2"
    title = name + " " + version

    #default grid size
    defaultGridSize = 40

    #grid-cell size
    cellHeight, cellWidth = 10, 10

    #grid size
    gridSize = defaultGridSize * cellHeight

    #menubar
    menubarHeight = 80
    #start/stop-button
    stButtonSize = 40
    stButtonPos = (gridSize / 2 - stButtonSize / 2, menubarHeight / 4 + gridSize)
    stButtonTrianglePoints = [(stButtonPos[0] + 10, stButtonPos[1] + 10),
                            (stButtonPos[0] + 30, stButtonPos[1] + 20),
                            (stButtonPos[0] + 10, stButtonPos[1] + 30)]
    #speed increase button
    spUpButtonSize = 40
    spUpButtonPos = (gridSize / 2 - spUpButtonSize / 2 + 100, menubarHeight / 4 + gridSize)
    #speed button
    spDownButtonSize = 40
    spDownButtonPos = (gridSize / 2 - spDownButtonSize / 2 - 100, menubarHeight / 4 + gridSize)

    #window 
    wHeight, wWidth = gridSize, gridSize + menubarHeight