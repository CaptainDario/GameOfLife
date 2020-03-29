
import pygame
import pygameMenu
import numpy as np
import random
import sys
import os

import IO
from game import runGameOfLife
from defaults import Defaults


COLOR_BACKGROUND = (60, 70, 70)
COLOR_SELECTED = (196, 60, 44)
COLOR_UNSELECTED = (255, 255, 255)
MENU_BACKGROUND_COLOR = (0,0,0)
MENU_HEADER_COLOR = (255, 145, 0)#"FF7400"
WINDOW_SIZE = (500, 500)#(Defaults.wHeight, Defaults.wWidth)

main_menu = None
boards_menu = None
surface = None


customMatrixXSize = Defaults.defaultGridSize
customMatrixYSize = Defaults.defaultGridSize
customMatrixBoundaryCondition = "absorbing"

customMatrix = None
matrixCreated = False

selectedBoundaryCondition = 'ABSORBING'
selectedMusic = 'miniBoss'



def set_X(val):
    """
    Sets the x size of a custom matrix.
    """
    
    global customMatrixXSize 
    customMatrixXSize = int(val)

def set_Y(val):
    """
    Sets the x size of a custom matrix.
    """

    global customMatrixYSize 
    customMatrixYSize = int(val)

def change_boundaryCondition(value : (), boundaryCondition : str):
    """
    Changes boundary Conditions.

    Args:
        val : Tuple containing the data of the selected object
        boundaryCondition : Optional parameter passed as argument to add_selector
    """

    global selectedBoundaryCondition

    selected, index = value
    print('Selected boundaryCondition: "{0}" ({1}) at index {2}'.format(selected, boundaryCondition, index))
    selectedBoundaryCondition = boundaryCondition

def changeMusic(value : (), music : str):
    """
    Changes music.

    Args:
        val : Tuple containing the data of the selected object
        boundaryCondition : Optional parameter passed as argument to add_selector
    """
    selected, index = value
    print('Selected boundaryCondition: "{0}" ({1}) at index {2}'.format(selected, music, index))
    selectedMusic = music


def createMatrix(_random : bool):
    """
    Create a matrix from the selected values.
    """

    global customMatrix
    global matrixCreated

    if(customMatrixXSize > 0 and customMatrixYSize > 0):
        
        customMatrix = np.zeros((customMatrixXSize, customMatrixYSize))
        if(_random):
            #randomize matrix
            for i in range(customMatrix.shape[0]):
                for j in range(customMatrix.shape[1]):
                    customMatrix[i][j] = random.randint(0,1)
        
        matrixCreated = True

def setLoadedMatrix(matrix : [[]], loadExample=False):
    '''
    Set the selected matix or open a file browser so that the user can select a saved matrix.
    '''

    global customMatrix
    global matrixCreated

    if(matrix is None):
        if(loadExample == False):
            matrix = IO.loadGridWithFileBrowser()
        elif(loadExample):
            matrix = IO.loadGridWithFileBrowser(_initialdir=os.path.join(os.getcwd(), "examples"))
        if(matrix is None):
            return

    customMatrix = matrix
    matrixCreated = True


def main_background():
    """
    Function used by menus, draw on background while menu is active.
    :return: None
    """
    global surface
    surface.fill(COLOR_BACKGROUND)

def main(test=True) -> [[]]:
    """


    Returns:
        The configured matrix.
    """


    global surface, matrixCreated

    pygame.init()

    # Create pygame screen and objects
    surface = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Game of Life')

    
    # Main menu
    main_menu = pygameMenu.Menu(surface,
                                back_box=False,
                                bgfun=main_background,
                                color_selected=COLOR_SELECTED,
                                font=pygameMenu.font.FONT_BEBAS,
                                font_color=COLOR_UNSELECTED,
                                font_size_title=32,
                                font_size=28,
                                menu_alpha=100,
                                menu_color=MENU_BACKGROUND_COLOR,
                                menu_color_title=MENU_HEADER_COLOR,
                                menu_height=int(WINDOW_SIZE[1]),
                                menu_width=int(WINDOW_SIZE[0]),
                                onclose=pygameMenu.events.DISABLE_CLOSE,
                                option_shadow=False,
                                title='Conways   Game   of   Life',
                                window_height=WINDOW_SIZE[1],
                                window_width=WINDOW_SIZE[0]
                                )
    new_board_menu = pygameMenu.Menu(surface,
                                back_box=False,
                                bgfun=main_background,
                                color_selected=COLOR_SELECTED,
                                font=pygameMenu.font.FONT_BEBAS,
                                font_color=COLOR_UNSELECTED,
                                font_size_title=32,
                                font_size=28,
                                menu_alpha=100,
                                menu_color=MENU_BACKGROUND_COLOR,
                                menu_color_title=MENU_HEADER_COLOR,
                                menu_height=int(WINDOW_SIZE[1]),
                                menu_width=int(WINDOW_SIZE[0]),
                                onclose=pygameMenu.events.DISABLE_CLOSE,
                                option_shadow=False,
                                title='new   board',
                                window_height=WINDOW_SIZE[1],
                                window_width=WINDOW_SIZE[0]
                                )
    load_board_menu = pygameMenu.Menu(surface,
                                back_box=False,
                                bgfun=main_background,
                                color_selected=COLOR_SELECTED,
                                font=pygameMenu.font.FONT_BEBAS,
                                font_color=COLOR_UNSELECTED,
                                font_size_title=32,
                                font_size=28,
                                menu_alpha=100,
                                menu_color=MENU_BACKGROUND_COLOR,
                                menu_color_title=MENU_HEADER_COLOR,
                                menu_height=int(WINDOW_SIZE[1]),
                                menu_width=int(WINDOW_SIZE[0]),
                                onclose=pygameMenu.events.DISABLE_CLOSE,
                                option_shadow=False,
                                title='load   board',
                                window_height=WINDOW_SIZE[1],
                                window_width=WINDOW_SIZE[0]
                                )
    options_menu = pygameMenu.Menu(surface,
                                back_box=False,
                                bgfun=main_background,
                                color_selected=COLOR_SELECTED,
                                font=pygameMenu.font.FONT_BEBAS,
                                font_color=COLOR_UNSELECTED,
                                font_size_title=32,
                                font_size=28,
                                menu_alpha=100,
                                menu_color=MENU_BACKGROUND_COLOR,
                                menu_color_title=MENU_HEADER_COLOR,
                                menu_height=int(WINDOW_SIZE[1]),
                                menu_width=int(WINDOW_SIZE[0]),
                                onclose=pygameMenu.events.DISABLE_CLOSE,
                                option_shadow=False,
                                title='options',
                                window_height=WINDOW_SIZE[1],
                                window_width=WINDOW_SIZE[0]
                                )
    
    #add main Menu Options
    main_menu.add_option('new   board', new_board_menu)
    main_menu.add_option('load   board', load_board_menu)
    main_menu.add_option('options', options_menu)
    main_menu.add_option('Quit', pygameMenu.events.EXIT)

    #add new board Menu Options
    new_board_menu.add_option('play', createMatrix, False)
    new_board_menu.add_option('play   random', createMatrix, True)
    new_board_menu.add_text_input('x-size: ',
                                 onchange=set_X,
                                 default=Defaults.defaultGridSize,
                                 maxchar=3,
                                 textinput_id='x_size',
                                 input_type=pygameMenu.locals.INPUT_INT,
                                 enable_selection=True)
    new_board_menu.add_text_input('y-size: ',
                                 onchange=set_Y,
                                 default=Defaults.defaultGridSize,
                                 maxchar=3,
                                 textinput_id='y_size',
                                 input_type=pygameMenu.locals.INPUT_INT,
                                 enable_selection=True)
    new_board_menu.add_selector('boundaryCondition',
                           [('absorbing', 'ABSORBING'),
                            ('periodic', 'PERIODIC'),
                            ('reflecting', 'REFLECTING')],
                           onchange=change_boundaryCondition,
                           selector_id='select_boundaryCondition')
    new_board_menu.add_option('Back', pygameMenu.events.BACK)

    #add load boards Menu Options
    load_board_menu.add_option('Load   example', setLoadedMatrix, None, True)
    load_board_menu.add_option('Load   from   file', setLoadedMatrix, None)
    load_board_menu.add_selector('boundaryCondition',
                           [('absorbing', 'ABSORBING'),
                            ('periodic', 'PERIODIC'),
                            ('reflecting', 'REFLECTING'),
                            ('expanding', 'EXPANDING')],
                           onchange=change_boundaryCondition,
                           selector_id='select_boundaryCondition')
    load_board_menu.add_option('Back', pygameMenu.events.BACK)
    
    options_menu.add_selector('Music',
                                [(i[:-len(Defaults.musicFileEnding)], str(c)) for c, i in enumerate(Defaults.musicFiles)],
                                onchange=changeMusic)
    options_menu.add_option('Back', pygameMenu.events.BACK)



    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:

        # Paint background
        main_background()

        events = pygame.event.get()

        # Main menu
        main_menu.mainloop(events, disable_loop=test)
        
        if(matrixCreated):
            pygame.display.quit()
            matrixCreated = False
            return customMatrix, selectedBoundaryCondition, selectedMusic




if __name__ == '__main__':
    main()
