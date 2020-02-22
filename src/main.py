import numpy as np

import menu
import game


def menuCycle():
    matrix = menu.main()
    ret = game.runGameOfLife(matrix)
    return ret


if __name__ == "__main__":
    
    newCycle = True
    while(newCycle):
        newCycle = menuCycle()