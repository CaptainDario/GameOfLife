from copy import deepcopy

from defaults import Defaults


class Grid():
    """
    The class for storing the current game state.

    attributes:
        defaultSize - default size of the grid
        currentTime - the current time step of the simulation (0 means that a start config needs to be drawn)
        grid        - 2D array to store the board (0 - dead | 1 - alive) (size: defaultSize x defaultSize)
    """

    def __init__(self):
        self.defaultSize = 8
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
        for cY, row in enumerate(tmpGrid):
            for cX, cell in enumerate(row):
                
                #apply the rules
                tmpGrid[cX][cY] = self.__rule1(cX, cY)

        self.grid = deepcopy(tmpGrid)
        self.currentTime += 1


    def __rule1(self, posX : int, posY : int) -> int:
        """
        Function to represent the first rule:
        A dead cell with exactly three living neighbors has to be reborn.

        Args:
            posX : the x position of the cell 
            posY : the y position of the cell

        Returns:
            The value of the cell for the next iteration
        """

        nextVal = 0

        #the cell needs to be dead
        if(self.grid[posX][posY] == 0):
            #exactly three neighbors have to be alive
            if(sum(self.__getNeighbors(posX, posY)) == 3):
                nextVal = 1

        return nextVal


    def __getNeighbors(self, posX : int, posY : int) -> []:
        """
        Returns the three upper neighbors.

        Args:
            posX : the x-position of the cell
            posY : the y-position of the cell

        Returns:
            A List containing the upper neighbors
        """

        #tmp list for all neighbors
        neighbors = []

        #UPPER
        #upper left 
        if(posY-1 > -1 and posX-1 > -1):
            neighbors.append(self.grid[posX-1][posY-1])
        #upper center
        if(posY-1 > -1):
            neighbors.append(self.grid[posX][posY-1])
        #upper right
        if(posY-1 > -1 and posX+1 < self.defaultSize):
            neighbors.append(self.grid[posX+1][posY-1])


        #SAME HEIGHT
        #lower left 
        if(posX-1 > -1):
            neighbors.append(self.grid[posX-1][posY])
        #lower right
        if(posX+1 < self.defaultSize):
            neighbors.append(self.grid[posX+1][posY])


        #LOWER
        #lower left 
        if(posY+1 < self.defaultSize and posX-1 > -1):
            neighbors.append(self.grid[posX-1][posY+1])
        #lower center
        if(posY+1 < self.defaultSize):
            neighbors.append(self.grid[posX][posY+1])
        #lower right
        if(posY+1 < self.defaultSize and posX+1 < self.defaultSize):
            neighbors.append(self.grid[posX+1][posY+1])

        print("X:", posX,"Y:", posY, neighbors)

        return neighbors