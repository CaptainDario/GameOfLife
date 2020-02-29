class Defaults():
    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    #Game info
    name = "Game Of Life"
    version = "v0.3.0"
    title = name + " " + version

    #boundary conditions (reflecting | absorbing | periodic)
    boundaryCondition  = "absorbing"

    #default grid size
    defaultGridSize = 10

    #grid-cell size
    cellHeight, cellWidth = 10, 10

    #grid size
    gridSize = 100 * cellHeight#defaultGridSize * cellHeight

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
    stButtonTrianglePoints = [(stButtonPos[0] + 10, stButtonPos[1] + 10),
                            (stButtonPos[0] + 30, stButtonPos[1] + 20),
                            (stButtonPos[0] + 10, stButtonPos[1] + 30)]
    #3 - speed increase button
    spUpButtonSize = defButtonSize
    spUpButtonPos = (buttonStartPosX + gapBetweenButtons * 2, menubarHeight / 4 + gridSize)
    # 4 - one-simulation-step-button
    oneStepButtonSize = defButtonSize
    oneStepButtonPos = (buttonStartPosX + gapBetweenButtons * 3, menubarHeight / 4 + gridSize)
    oneStepButtonTrianglePoints = [(oneStepButtonPos[0] + 20, oneStepButtonPos[1] + 10),
                                (oneStepButtonPos[0] + 30, oneStepButtonPos[1] + 20),
                                (oneStepButtonPos[0] + 20, oneStepButtonPos[1] + 30)]
    menuButtonSize = defButtonSize
    menuButtonPos = (40, menubarHeight / 4 + gridSize)


    #window 
    wHeight, wWidth = gridSize + menubarHeight, gridSize