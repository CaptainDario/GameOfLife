

class Grid():
    """
    The class for storing the current game state.

    attributes:
        defaultSize - default size of the grid
        grid        - 2D array to store the board (0 - dead | 1 - alive)
    """

    def __init__(self):
        self.defaultSize = 32
        self.grid = [[0 for j in range(self.defaultSize)] for i in range(self.defaultSize)]

        self.grid[13][5] = 1