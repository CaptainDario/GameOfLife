import pygame




class Camera():
    """
    A class representing the camera which renders the game world.
    """


    def __init__(self, width, height):
        self.width = width
        self.height = height

        #position
        self.pos = (0, 0)

        #zooming
        self.currentZoom = 50
        self.zoomOutLimit = 50 
        self.zoomInLimit = -7


    def setPos(self, newPos : (int, int)):
        """
        Set the camera position to a new value.

        Args:
            position : the position where the camera should be located in the next frame.
        """

        self.pos = newPos

    def zoomIn(self):
        """
        Zoom in (make the grid larger) only if a certain zoom limit is not reached.
        """

        if(self.currentZoom > self.zoomInLimit):
            self.currentZoom -= 1
    
    def zoomOut(self):
        """
        Zoom in (make the grid larger) only if a certain zoom limit is not reached.
        """

        if(self.currentZoom < self.zoomOutLimit):
            self.currentZoom += 1