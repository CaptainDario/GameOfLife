import numpy as np

from copy import deepcopy

from defaults import Defaults


class Grid():
    """
    The class for storing the current game state.

    attributes:
        defaultSize - default size of the grid
        currentTime - the current time step of the simulation (0 means that a start config needs to be drawn)
        grid        - numpy matrix to store the board (0 - dead | 1 - alive) (size: defaultSize x defaultSize)
    """

    def __init__(self):
        self.currentSize = Defaults.defaultGridSize
        self.currentTime = 0
        self.grid = np.zeros((self.currentSize, self.currentSize))

        #self.grid[13][5] = 1

    def applyRules(self):
        """
        Apply the rules to all cells.
        """

        #copy current state
        futureGrid = deepcopy(self.grid)

        #iterate ove all cells
        for cY, row in enumerate(futureGrid):
            for cX, cell in enumerate(row):
                futureGrid[cX][cY] = 0 if self.__rule2(cX, cY) is not None else futureGrid[cX][cY]
                futureGrid[cX][cY] = 0 if self.__rule4(cX, cY) is not None else futureGrid[cX][cY]

                futureGrid[cX][cY] = 1 if self.__rule1(cX, cY) is not None else futureGrid[cX][cY]
                futureGrid[cX][cY] = 1 if self.__rule3(cX, cY) is not None else futureGrid[cX][cY]

        self.grid = deepcopy(futureGrid)
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

        nextVal = None

        #the cell needs to be dead
        if(self.grid[posX][posY] == 0):
            #exactly three neighbors have to be alive
            if(self.__getNeighbors(posX, posY) == 3):
                nextVal = 1

        return nextVal

    def __rule2(self, posX : int, posY : int) -> int:
        """
        Function to represent the second rule:
        A living cell with less than two living neighbors will die because of loneliness.

        Args:
            posX : the x position of the cell 
            posY : the y position of the cell

        Returns:
            The value of the cell for the next iteration
        """

        nextVal = None

        #the cell needs to be alive
        if(self.grid[posX][posY] == 1):
            #exactly three neighbors have to be alive
            if(self.__getNeighbors(posX, posY) < 2):
                nextVal = 0

        return nextVal

    def __rule3(self, posX : int, posY : int) -> int:
        """
        Function to represent the third rule:
        A living cell with exactly two or three living neighbors will stay a life.

        Args:
            posX : the x position of the cell 
            posY : the y position of the cell

        Returns:
            The value of the cell for the next iteration
        """

        nextVal = None

        #the cell needs to be alive
        if(self.grid[posX][posY] == 1):
            #exactly three neighbors have to be alive
            if(self.__getNeighbors(posX, posY) == 2 or
                self.__getNeighbors(posX, posY) == 3):
                nextVal = 1

        return nextVal

    def __rule4(self, posX : int, posY : int) -> int:
        """
        Function to represent the forth rule:
        A living cell with more than three living neighbors will die.

        Args:
            posX : the x position of the cell 
            posY : the y position of the cell

        Returns:
            The value of the cell for the next iteration
        """

        nextVal = None

        #the cell needs to be alive
        if(self.grid[posX][posY] == 1):
            #exactly three neighbors have to be alive
            if(self.__getNeighbors(posX, posY) > 3):
                nextVal = 0

        return nextVal

    def __getNeighbors(self, posX : int, posY : int) -> []:
        """
        Returns the three upper neighbors.

        Args:
            posX : the x-position of the cell
            posY : the y-position of the cell

        Returns:
            Amount of living neighbors
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
        if(posY-1 > -1 and posX+1 < self.currentSize):
            neighbors.append(self.grid[posX+1][posY-1])


        #SAME HEIGHT
        #lower left 
        if(posX-1 > -1):
            neighbors.append(self.grid[posX-1][posY])
        #lower right
        if(posX+1 < self.currentSize):
            neighbors.append(self.grid[posX+1][posY])


        #LOWER
        #lower left 
        if(posY+1 < self.currentSize and posX-1 > -1):
            neighbors.append(self.grid[posX-1][posY+1])
        #lower center
        if(posY+1 < self.currentSize):
            neighbors.append(self.grid[posX][posY+1])
        #lower right
        if(posY+1 < self.currentSize and posX+1 < self.currentSize):
            neighbors.append(self.grid[posX+1][posY+1])

        #print("X:", posX,"Y:", posY, neighbors)

        return sum(neighbors)

    def __mergeRuleMatrices(self, r1 : [[int]], r2 : [[int]], r3 : [[int]], r4 : [[int]]) -> [[int]]:
        """


        Args:

        Returns:

        """

        return r1 + r2 + r3 + r4 