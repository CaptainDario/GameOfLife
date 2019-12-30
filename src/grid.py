from copy import deepcopy

class Grid():
    """
    The class for storing the current game state.

    attributes:
        defaultSize - default size of the grid
        grid        - 2D array to store the board (0 - dead | 1 - alive)
    """

    def __init__(self):
        self.defaultSize = 32
        self.currentTime = 0
        self.grid = [[0 for j in range(self.defaultSize)] for i in range(self.defaultSize)]

        #self.grid[13][5] = 1

    def applyRules(self):
        """
        Apply the rules to all cells.
        """

        #copy current state
        tmpGrid = deepcopy(self.grid)

        #iterate ove all cells
        for cX, row in enumerate(self.grid):
            for cY, cell in enumerate(row):
                
                #apply the rules
                self.__rule1(cX, cY, cell)

        self.currentTime += 1


    def __rule1(self, posX, posY, cell):
        """
        A dead cell with exactly three living neighbors has to be reborn.
        """

        #the cell needs to be dead
        if(cell == 0):
            #exactly three neighbors have to be alive
            if():
                cell = 1
