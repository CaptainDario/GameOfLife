import pygame


class DrawUtil():
    """
    Utility class for drawing.
    """

    @staticmethod
    def drawRectWithBorder(screen, bColor, fColor, posX, posY, height, width, bWidth):
        """
        Draws a rect with an outline.

        Args:
            screen - the pygame canvas object 
            bColor - the border color
            fColor - the fill color
            posX   - the x position for the square to draw
            posY   - the y position for the square to draw
            height - the height of the square to draw
            width  - the width of the square to draw
            bWidth - the width of the square's border (border is not additive [acts like padding])
        """
        
        #draw outline rect 
        pygame.draw.rect(screen, bColor, (posX, posY, height, width))
        #draw fill rect
        pygame.draw.rect(screen, fColor, (posX + bWidth, posY + bWidth, height - bWidth * 2, width - bWidth * 2))