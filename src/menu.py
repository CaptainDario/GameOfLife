
import pygame
import pygameMenu
import numpy as np
import random

from game import runGameOfLife
from defaults import Defaults


COLOR_BACKGROUND = (60, 70, 70)
COLOR_SELECTED = (196, 60, 44)
COLOR_UNSELECTED = (255, 255, 255)
MENU_BACKGROUND_COLOR = (0,0,0)
MENU_HEADER_COLOR = (255, 145, 0)#"FF7400"
WINDOW_SIZE = (500, 500)#(Defaults.wHeight, Defaults.wWidth)
BOUNDARY_CONDITION = ['ABSORBING']

main_menu = None
boards_menu = None
surface = None

defaultGrid1 = np.zeros((Defaults.defaultGridSize, Defaults.defaultGridSize))
randomGrid = np.zeros((Defaults.defaultGridSize, Defaults.defaultGridSize))

for i in range(randomGrid.shape[0]):
    for j in range(randomGrid.shape[1]):
        randomGrid[i][j] = random.randint(0,1)

for i in range(defaultGrid1.shape[0]):
    defaultGrid1[i][i] = 1
    defaultGrid1[i][defaultGrid1.shape[0]-i-1] = 1

def change_boundaryCondition(value, boundaryCondition):
    """
    Changes boundary Conditions.
    :param value: Tuple containing the data of the selected object
    :type value: tuple
    :param boundaryCondition: Optional parameter passed as argument to add_selector
    :type boundaryCondition: basestring
    :return: None
    """
    selected, index = value
    print('Selected boundaryCondition: "{0}" ({1}) at index {2}'.format(selected, boundaryCondition, index))
    BOUNDARY_CONDITION[0] = boundaryCondition

def main_background():
    """
    Function used by menus, draw on background while menu is active.
    :return: None
    """
    global surface
    surface.fill(COLOR_BACKGROUND)

def main(test=False) -> [[]]:
    """


    Returns:
        The configured matrix.
    """


    global surface

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
    boards_menu = pygameMenu.Menu(surface,
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
    
    #add main Menu Options
    main_menu.add_option('new   board', new_board_menu)
    main_menu.add_option('load   board', boards_menu)
    main_menu.add_option('Quit', pygameMenu.events.EXIT)

    #add load boards Menu Options
    boards_menu.add_option('default   Example   1',runGameOfLife ,defaultGrid1)
    boards_menu.add_option('default   Example   2', runGameOfLife, defaultGrid1)
    boards_menu.add_option('Random   Board', runGameOfLife, randomGrid)
    boards_menu.add_option('Back', pygameMenu.events.BACK)
    
    #add new board Menu Options
    new_board_menu.add_option('play', runGameOfLife, np.zeros((10, 10)))
    new_board_menu.add_text_input('x-size: ',
                                 default=Defaults.defaultGridSize,
                                 maxchar=3,
                                 textinput_id='x_size',
                                 input_type=pygameMenu.locals.INPUT_INT,
                                 enable_selection=False)
    new_board_menu.add_text_input('y-size: ',
                                 default=Defaults.defaultGridSize,
                                 maxchar=3,
                                 textinput_id='y_size',
                                 input_type=pygameMenu.locals.INPUT_INT,
                                 enable_selection=False)
    new_board_menu.add_selector('boundaryCondition',
                           [('absorbing', 'ABSORBING'),
                            ('periodic', 'PERIODIC'),
                            ('reflecting', 'REFLECTING'),
                            ('expanding', 'EXPANDING')],
                           onchange=change_boundaryCondition,
                           selector_id='select_boundaryCondition')
    new_board_menu.add_option('Back', pygameMenu.events.BACK)

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:

        # Paint background
        main_background()

        # Application events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
                return -1

        # Main menu
        main_menu.mainloop(events, disable_loop=test)


if __name__ == '__main__':
    main()
