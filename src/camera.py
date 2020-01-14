import pygame




class Camera():
    """
    A class representing the camera which renders the game world.
    """


    def __init__(self, width, height, currentZoom):
        self.width = width
        self.height = height

        #position
        self.pos = (0, 0)

        #zooming
        self.currentZoom = currentZoom
        self.zoomOutLimit = 100
        self.zoomInLimit = 3


    def setPos(self, newPos : (int, int)):
        """
        Set the camera position to a new value.

        Args:
            position : the position where the camera should be located in the next frame.
        """

        self.pos = newPos