import numpy as np

import menu
import game


def menuCycle():
    matrix, boundaryCondition, music = menu.main()
    matrix = np.array(matrix)
    ret = game.runGameOfLife(matrix, boundaryCondition, music)
    return ret


if __name__ == "__main__":
    
    newCycle = True
    while(newCycle):
        newCycle = menuCycle()