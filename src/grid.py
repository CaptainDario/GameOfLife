import math
import multiprocessing

import numpy as np

from copy import deepcopy
from itertools import product

from defaults import Defaults


class Grid():
    """
    The class for storing the current game state.

    attributes:
        defaultSize        - default size of the grid
        currentTime        - the current time step of the simulation (0 means that a start config needs to be drawn)
        grid               - numpy matrix to store the board (0 - dead | 1 - alive) (size: defaultSize x defaultSize)
        fullRedrawRequired - if a full update is required (wipe screen blank and redraw everything [computationally expensive])
        redrawRequired     - if a partial update is required
        cellsToUpdate      - all cells which need to be redrawn next frame
    """

    def __init__(self):
        self.currentSizeX = 7 #Defaults.defaultGridSize
        self.currentSizeY = 19 #Defaults.defaultGridSize
        self.currentTime = 0
        self.grid = grid
        self.fullRedrawRequired = False
        self.redrawRequired = False
        self.cellsToUpdate = []

        # when board initialized do a full redraw
        self.fullRedraw()


    def fullRedraw(self):
        """
        Tells the grid that a complete update of the graphics is required.
        Calling this function often is computationally very expensive.
        """

        self.cellsToUpdate = [(x, y) for y in range(self.currentSizeY) for x in range(self.currentSizeX)]
        self.fullRedrawRequired = True
        self.redrawRequired = True

    def applyRules(self):
        """
        Apply the rules to all cells.
        """

        #if it is the initial board setup (timestep 0 --> 1) check if board should be resized
        #if(self.currentTime == 0):
        #    self.grid = self.__resizeGrid(self.grid, True, True, True, True)
        #    self.grid = self.__resizeGrid(self.grid, True, True, True, True)

        #copy current state
        futureGrid = deepcopy(self.grid)

        # sides which maybe need to be enlargened
        left, top, right, bottom = False, False, False, False

        #single core calculations
        if(True):
            #iterate ove all cells
            for cX in range(0, self.currentSizeX):
                #tmp sides 
                for cY in range(0, self.currentSizeY):
                    
                    newCell, _left, _top, _right, _bottom  = self.__processCell(cX, cY)
                    futureGrid[cX][cY] = newCell

                    #remember that this side(s) need to be expanded
                    left   = True if _left else left
                    top    = True if _top else top
                    right  = True if _right else right
                    bottom = True if _bottom else bottom

        #resize if neccessary
        if(left or top or right or bottom):
            pass
            #futureGrid = self.__resizeGrid(futureGrid, left, top, right, bottom)

        #copy the new grid to the old and increase the time
        self.grid = deepcopy(futureGrid)
        self.currentTime += 1


    def __processCell(self, cX, cY) -> (int, bool, bool, bool, bool):
        """
        
        Apply the rules to all cells.
        """

        #the value of the new cell
        currentCell, newCell = self.grid[cX][cY], self.grid[cX][cY]

        #check if this cell is near the border
        _left, _top, _right, _bottom = False, False, False, False

        neighbors = self.__boundaryCondition(cX, cY) - newCell

        #apply the rules
        if(currentCell == 0):
            if(neighbors == 3):
                newCell = 1

        if(currentCell == 1):
            if(neighbors < 2):
                newCell = 0
            if(neighbors == 2 or neighbors == 3):
                newCell = 1
            if(neighbors > 3):
                newCell = 0

        if(newCell == 1):
            if(cY <= 2):
                _top = True
            if(cY >= self.currentSizeY - 2):
                _bottom = True
            if(cX <= 2):
                _left = True
            if(cX >= self.currentSizeX - 2):
                _right = True

        #redraw a cell if its state has changed
        #and a full redraw is not necessary 
        if newCell != self.grid[cX][cY] and \
            not self.fullRedrawRequired:
            self.redrawRequired = True
            self.cellsToUpdate.append((cX, cY))

        return newCell, _left, _top, _right, _bottom

    def __boundaryCondition(self, cX : int, cY : int):
        """
        Calculate the next cell value with the corresponding boundary condition.

        Args:
            cX : the x-position of the cell
            cY : the y-position of the cell

        Returns:
            the value of all neighbors
        """

        ret = 0

        if(Defaults.boundaryCondition == "absorbing"):
            lMarginX, lMarginY, rMarginX, rMarginY = 1, 1, 2, 2
            if(cX == 0):
                lMarginX = 0
            elif(cY == 0):
                lMarginY = 0
            if(cX == self.currentSizeX):
                rMarginX = 1
            elif(cY == self.currentSizeY):
                rMarginY = 1
                
            ret = self.grid[cX - lMarginX: cX + rMarginX, cY - lMarginY : cY + rMarginY].sum()

        elif(Defaults.boundaryCondition == "periodic"):
            for x in range(cX - 1,cX + 2):
                tmpX = x
            if(x > self.currentSizeX):
                tmpX = x - self.currentSizeX
            if(x < 0):
                tmpX = x + self.currentSizeX
                for y in range(cY - 1,cY + 2):
                    tmpY = y
                    if(y > self.currentSizeY):
                        tmpY = y - self.currentSizeY
                    if(y < 0):
                        tmpY = y + self.currentSizeY

                    ret += self.grid[tmpX][tmpY]
        #reflecting
        else:
            pass


        return ret



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

        #set the new size of the grid
        self.currentSizeX += left + right
        self.currentSizeY += top + bottom

        if(left):
            tmp = np.zeros((1, len(grid[0])))
            grid = np.vstack((grid, tmp))
        if(top):
            tmp = [[0] for i in range(len(grid))]
            grid = np.hstack((grid, tmp))
        if(right):
            tmp = np.zeros((1, len(grid[0])))
            grid = np.vstack((tmp, grid))
        if(bottom):
            tmp = [[0] for i in range(len(grid))]
            grid = np.hstack((tmp, grid))

        #set the new gridsize
        self.cellsToUpdate.resize(self.currentSizeX * self.currentSizeY, refcheck=False)

        #grid got resize --> redraw whole grid
        self.fullRedraw()

        return grid








