import os



class Defaults():
    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    #Game info
    name = "Game Of Life"
    version = "v1.0.0"
    title = name + " " + version

    #boundary conditions (reflecting | absorbing | periodic)
    boundaryCondition  = "absorbing"

    #default grid size
    defaultGridSize = 10

    #grid-cell size
    cellHeight, cellWidth = 10, 10

    #grid size
    gridSize = 50 * cellHeight#defaultGridSize * cellHeight

    #menubar
    menubarHeight = 80
    defButtonSize = 40
    buttonAmount = 4
    gapBetweenButtons = defButtonSize + defButtonSize / 10
    buttonStartPosX = (gridSize / 2) - (buttonAmount * gapBetweenButtons) / 2

    # 1 - speed decrease button
    spDownButtonSize = defButtonSize
    spDownButtonPos = (buttonStartPosX + gapBetweenButtons * 0, menubarHeight / 4 + gridSize)
    # 2 - start/stop-button
    stButtonSize = defButtonSize
    stButtonPos = (buttonStartPosX + gapBetweenButtons * 1, menubarHeight / 4 + gridSize)
    
    #3 - speed increase button
    spUpButtonSize = defButtonSize
    spUpButtonPos = (buttonStartPosX + gapBetweenButtons * 2, menubarHeight / 4 + gridSize)
    # 4 - one-simulation-step-button
    oneStepButtonSize = defButtonSize
    oneStepButtonPos = (buttonStartPosX + gapBetweenButtons * 3, menubarHeight / 4 + gridSize)
    # 5 - Save grid Button
    saveGridButtonSize = defButtonSize
    saveGridButtonPos = (buttonStartPosX + gapBetweenButtons * 4, menubarHeight / 4 + gridSize)
    
    menuButtonSize = defButtonSize
    menuButtonPos = (40, menubarHeight / 4 + gridSize)


    #window 
    wHeight, wWidth = gridSize + menubarHeight, gridSize


    #simulation
    simulationSpeed = 180
    speedSteps = 1

    #music
    musicFiles = os.listdir(os.path.join(os.getcwd(), "music"))
    musicFileEnding = ".mp3"