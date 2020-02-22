import math

import numpy as np

from copy import deepcopy

from defaults import Defaults


class Grid():
    """
    The class for storing the current game state.

    attributes:
        defaultSize        - default size of the grid
        currentTime        - the current time step of the simulation (0 means that a start config needs to be drawn)
        grid               - numpy matrix to store the board (0 - dead | 1 - alive) (size: defaultSize x defaultSize)
        fullRedrawRequired - if a full update is required (wipe screen blank and redraw everything [computationally expensive])
        cellsToUpdate      - all cells which need to be redrawn next frame
    """

    def __init__(self, grid=None):
        self.currentSize = Defaults.defaultGridSize
        self.currentTime = 0

        if(type(grid) == type(None)):
            self.grid = np.zeros((self.currentSize, self.currentSize))
        else:
            self.grid = grid
        self.fullRedrawRequired = False
        self.cellsToUpdate = []

        self.fullRedraw()


    def fullRedraw(self):
        """
        Tells the grid that a complete update of the graphics is required.
        Calling this function often is computationally very expensive.
        """

        self.fullRedrawRequired = True
        self.cellsToUpdate = [(x, y) for y in range(self.currentSize) for x in range(self.currentSize)]

    def applyRules(self):
        """
        Apply the rules to all cells.
        """

        #if it is the initial board setup (timestep 0 --> 1) check if board should be resized
        if(self.currentTime == 0):
            self.grid = self.__resizeGrid(self.grid, True, True, True, True)
            self.grid = self.__resizeGrid(self.grid, True, True, True, True)

        #copy current state
        futureGrid = deepcopy(self.grid)

        # sides which maybe need to be enlargened
        left, top, right, bottom = False, False, False, False

        #iterate ove all cells
        for cY, row in enumerate(futureGrid):
            for cX, cell in enumerate(row):
                #check if this cell is near the border
                _left, _top, _right, _bottom = False, False, False, False

                #apply the rules
                r1, r2 = self.__rule1(cX, cY), self.__rule2(cX, cY)
                r3, r4 = self.__rule3(cX, cY), self.__rule4(cX, cY)
                if(r2 is not None):
                    futureGrid[cX][cY] = 0
                elif(r4 is not None):
                    futureGrid[cX][cY] = 0
                elif(r1 is not None):
                    futureGrid[cX][cY] = 1
                    # check if the cell is to close to the border
                    _left, _top, _right, _bottom = self.__cellIsNearBorder(cX, cY)
                elif(r3 is not None):
                    futureGrid[cX][cY] = 1
                    #check if the cell is too close to the border
                    _left, _top, _right, _bottom = self.__cellIsNearBorder(cX, cY)

                #remember that this side(s) need to be expanded
                left   = True if _left else left
                top    = True if _top else top
                right  = True if _right else right
                bottom = True if _bottom else bottom

                #redraw a cell if its state has changed
                #and a full redraw is not necessary 
                if futureGrid[cX][cY] != self.grid[cX][cY] and \
                   not self.fullRedrawRequired:
                    self.cellsToUpdate.append((cX, cY))

        #resize if necessary
        if(left or top or right or bottom):
            futureGrid = self.__resizeGrid(futureGrid, left, top, right, bottom)

        #copy the new grid to the old and increase the time
        self.grid = deepcopy(futureGrid)
        self.currentTime += 1


    def __cellIsNearBorder(self, _x : int, _y : int) -> (bool, bool, bool, bool):
        """
        Check if the cell is near one of the borders.

        Args:
            _x - the x-value of the cell
            _y - the y-value of the cell

        Returns:
            All directions where the cell may be near the border(left, top, right, bottom)
        """

        left, top, right, bottom = False, False, False, False

        if(_x <= 2):
            left = True
        if(_y <= 2):
            top = True
        if(_x >= self.currentSize - 3):
            right = True
        if(_y >= self.currentSize - 3):
            bottom = True

        #print("x:", _x, "y:", _y, left, top, right, bottom)
        return left, top, right, bottom

    def __resizeGridKeepSquare(self, left=False, top=False, right=False, bottom=False) -> (bool, bool, bool, bool):
        """
        Ensures that all the grid will be still a square after the resize.
        The rules if only one side gets selected are:
            left   --> top
            top    --> right
            right  --> bottom
            bottom --> left
        If 2 sides are selected it will be checked if the grid remains square with this selection if not
        all sides will be expanded
        If 3 sides are selected everything will be expanded.
        Also sets the new grid size.

        Args:
            left   - should to the left be a column appended 
            top    - should to the top be a column appended 
            right  - should to the right be a column appended 
            bottom - should to the bottom be a column appended

        Returns:
            Tuple with the sides on which rows/columns should be added (left, top, right, bottom).
        """

        trueCount = [top, right, bottom, left].count(True)

        #nothing set to True 
        if(trueCount > 0):
            #three are set to True --> set the forth to true
            if(trueCount == 3):
                left, top, right, bottom = False, False, False, False
            elif(trueCount == 2):
                if(left and right):
                    top = True
                    bottom = True
                if(top and bottom):
                    left = True
                    right = True
            #only one side is True --> set accordingly to the pattern
            elif(trueCount == 1):
                if(left):
                    top = True
                elif(top):
                    right = True
                elif(right):
                    bottom = True
                elif(bottom):
                    left = True

        return (left, top, right, bottom)

    def __resizeGrid(self, grid : np.array, left : bool, top : bool, right : bool, bottom : bool) -> np.array:
        """
        Resize the given grid on the given sides

        Args:
            grid   - the grid which should be resized
            left   - if the left side should be made larger
            top    - if the top side should be made larger
            right  - if the right side should be made larger
            bottom - if the bottom side should be made larger

        Returns:
            The resized grid 
        """

        left, top, right, bottom = self.__resizeGridKeepSquare(left, top, right, bottom)

        if(right):
            tmp = np.zeros((1, len(grid[0])))
            grid = np.vstack((grid, tmp))
        if(bottom):
            tmp = [[0] for i in range(len(grid))]
            grid = np.hstack((grid, tmp))
        if(left):
            tmp = np.zeros((1, len(grid[0])))
            grid = np.vstack((tmp, grid))
        if(top):
            tmp = [[0] for i in range(len(grid))]
            grid = np.hstack((tmp, grid))

        #set the new gridsize
        test = math.floor([top, right, bottom, left].count(True) // 2)
        self.currentSize += test

        #grid got resize --> redraw whole grid
        self.fullRedraw()

        return grid


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



