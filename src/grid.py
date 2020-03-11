import math
import multiprocessing

import numpy as np

from copy import deepcopy
from itertools import product
from joblib import Parallel, delayed

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

    def __init__(self, grid : [[]], boundaryCondition : str):
        self.currentSizeX = len(grid)
        self.currentSizeY = len(grid[0])
        self.currentTime = 0
        self.grid = np.array(grid, copy=True)
        self.boundaryCondition = boundaryCondition
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

        #copy current state
        futureGrid = deepcopy(self.grid)

        #iterate ove all cells
        for cX in range(0, self.currentSizeX):
            futureGrid[cX] = Parallel(n_jobs=-1)(delayed(self.__processCell)(cX, cY) for cY in range(self.currentSizeY))
        
        #copy the new grid to the old and increase the time
        self.grid = deepcopy(futureGrid)
        self.currentTime += 1

    def __processCell(self, cX, cY) -> (int):
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

        return newCell#, _left, _top, _right, _bottom

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







