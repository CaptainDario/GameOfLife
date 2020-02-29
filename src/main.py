import numpy as np

import menu
import game


def menuCycle():
    matrix = menu.main()
    ret = game.runGameOfLife(matrix)
    return ret


if __name__ == "__main__":
    
    
    matrix = menu.main()
    matrix = np.array(matrix)
    game.runGameOfLife(matrix)

    #newCycle = True
    #while(newCycle):
    #    newCycle = menuCycle()