
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
    cellHeight, cellWidth = 25, 25

    #window 
    wHeight, wWidth = defaultGridSize * cellHeight, defaultGridSize * cellWidth