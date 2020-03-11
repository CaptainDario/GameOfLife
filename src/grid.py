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

    def __init__(self, grid : [[]], boundaryCondition : str):
        self.currentSizeX = len(grid)
        self.currentSizeY = len(grid[0])
        self.currentTime = 0
        self.grid = np.array(grid, copy=True)

        self.boundaryCondition = boundaryCondition
        if(boundaryCondition == "periodic"):
            self.updatePriodicGrid()
        self.fullRedrawRequired = False
        self.redrawRequired = False
        self.cellsToUpdate = []

        # when board initialized do a full redraw
        self.fullRedraw()

    def updatePriodicGrid(self):
        """
        Updates the references of the periodic grid.
        """

        self.periodicGrid = [[self.grid[::-1], self.grid, self.grid[::-1]],
                            [self.grid, self.grid, self.grid],
                            [self.grid[::-1], self.grid, self.grid[::-1]]]



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
        self.updatePriodicGrid()
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

        if(self.boundaryCondition == "absorbing"):
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

        elif(self.boundaryCondition == "periodic"):
            r"""
         0: 0----  1----  2----
            |123|  |123|  |123|
            |456|  |456|  |456|
            |789|  |789|  |789|
            -----  -----  -----
                 \   |   /
                  \  |  /
         1: 0----  1----  2----
            |123|  |123|  |123|
            |456|--|456|--|456|
            |789|  |789|  |789|
            -----  -----  -----
                  /  |  \
                 /   |   \
         2: 0----  1----  2----
            |123|  |123|  |123|
            |456|  |456|  |456|
            |789|  |789|  |789|
            -----  -----  -----
            """

            overR, overL, overB, overT = 0, 0, 0, 0

            if(cX == self.currentSizeX - 1):
                overR = 1
            elif(cX == 0):
                overL = 1
            if(cY == self.currentSizeY - 1):
                overB = 1
            elif(cY == 0):
                overT = 1

            #get square from base
            ret += self.periodicGrid[1][1][cX-1+overL : cX+2-overR,
                                            cY-1+overT : cY+2-overB].sum()

            #get periodic squares
            #TOP
            if(overT and not overR and not overB and not overL):
                ret += self.periodicGrid[0][1][cX-1 : cX+2, len(self.grid[0]) - 1].sum()
            #RIGHT
            if(overR and not overB and not overL and not overT):
                ret += self.periodicGrid[1][2][0, cY-1 : cY+2].sum()
            #BOTTOM
            if(overB and not overL and not overT and not overR):
                ret += self.periodicGrid[2][1][cX-1 : cX+2, 0].sum()
            #LEFT
            if(overL and not overT and not overR and not overB):
                ret += self.periodicGrid[1][0][len(self.grid) -1, cY-1 : cY+2].sum()

            #TOP and RIGHT
            if(overT and overR):
                ret += self.periodicGrid[0][1][cX-1 : cX+1, len(self.grid[0]) - 1].sum()    #T
                ret += self.periodicGrid[1][2][0, cY : cY+2].sum()                        #R
                ret += self.periodicGrid[0][2][len(self.grid[0]) - 1, 0].sum()                 #C
            #RIGHT and BOTTOM
            if(overR and overB):
                ret += self.periodicGrid[1][2][0, cY-1 : cY+2].sum()
                ret += self.periodicGrid[2][1][cX-1 : cX+2, 0].sum()
                ret += self.periodicGrid[0][2][0, 0].sum()
            #BOTTOM and LEFT
            if(overB and overL):
                ret += self.periodicGrid[2][1][cX : cX+2, 0].sum()
                ret += self.periodicGrid[1][0][len(self.grid) -1, cY-1 : cY+1].sum()
                ret += self.periodicGrid[0][2][0, len(self.grid) - 1].sum()
            #LEFT and TOP
            if(overL and overT):
                ret += self.periodicGrid[1][0][len(self.grid) -1, cY-1 : cY+2].sum()
                ret += self.periodicGrid[0][1][cX-1 : cX+2, len(self.grid[0]) - 1].sum()
                ret += self.periodicGrid[0][2][len(self.grid) - 1, len(self.grid) - 1].sum()


        #reflecting
        else:
            """
            -----      -----
            |123|      |321|
            |456|  --> |654|
            |789|      |987|
            -----      -----
            """
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








