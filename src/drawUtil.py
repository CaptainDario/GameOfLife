import pygame


class DrawUtil():
    """
    Utility class for drawing pygame objects.
    """

    @staticmethod
    def drawRectWithBorder(screen, bColor, fColor, posX, posY, height, width, bWidth):
        """
        Draws a rect with an outline.

        Args:

        """
        
        #draw outline rect 
        pygame.draw.rect(screen, bColor, (posX, posY, height, width))
        #draw fill rect
        pygame.draw.rect(screen, fColor, (posX + bWidth, posY + bWidth, height - bWidth * 2, width - bWidth * 2))