
import pygame
import pygameMenu

from main import runGameOfLife
from defaults import Defaults


COLOR_BACKGROUND = (60, 70, 70)
COLOR_SELECTED = (196, 60, 44)
COLOR_UNSELECTED = (255, 255, 255)
MENU_BACKGROUND_COLOR = (0,0,0)
WINDOW_SIZE = (Defaults.wHeight, Defaults.wWidth)
BOUNDARY_CONDITION = ['ABSORBING']

main_menu = None
boards_menu = None
surface = None

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


def main(test=False):

    global surface

    pygame.init()

    # Create pygame screen and objects
    surface = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Game of Life')

    
    # Main menu
    main_menu = pygameMenu.Menu(surface,
                                bgfun=main_background,
                                color_selected=COLOR_SELECTED,
                                font=pygameMenu.font.FONT_BEBAS,
                                font_color=COLOR_UNSELECTED,
                                font_size_title=32,
                                font_size=28,
                                menu_alpha=100,
                                menu_color=MENU_BACKGROUND_COLOR,
                                menu_height=int(WINDOW_SIZE[1] * 0.5),
                                menu_width=int(WINDOW_SIZE[0] * 0.8),
                                onclose=pygameMenu.events.DISABLE_CLOSE,
                                option_shadow=False,
                                title='Cornwys   Game   of   Life',
                                window_height=WINDOW_SIZE[1],
                                window_width=WINDOW_SIZE[0]
                                )
    boards_menu = pygameMenu.Menu(surface,
                                bgfun=main_background,
                                color_selected=COLOR_SELECTED,
                                font=pygameMenu.font.FONT_BEBAS,
                                font_color=COLOR_UNSELECTED,
                                font_size_title=32,
                                font_size=28,
                                menu_alpha=100,
                                menu_color=MENU_BACKGROUND_COLOR,
                                menu_height=int(WINDOW_SIZE[1] * 0.5),
                                menu_width=int(WINDOW_SIZE[0] * 0.8),
                                onclose=pygameMenu.events.DISABLE_CLOSE,
                                option_shadow=False,
                                title='load   board',
                                window_height=WINDOW_SIZE[1],
                                window_width=WINDOW_SIZE[0]
                                )
    
    #add main Menu Options
    main_menu.add_option('Play', runGameOfLife)
    main_menu.add_option('load   board', boards_menu)
    main_menu.add_selector('boundaryCondition',
                           [('absorbing', 'ABSORBING'),
                            ('periodic', 'PERIODIC'),
                            ('reflecting', 'REFLECTING'),
                            ('expanding', 'EXPANDING')],
                           onchange=change_boundaryCondition,
                           selector_id='select_boundaryCondition')
    main_menu.add_option('Quit', pygameMenu.events.EXIT)

    #add load boards Menu Options
    boards_menu.add_option('default   Example   1', runGameOfLife)
    boards_menu.add_option('default   Example   2', runGameOfLife)
    boards_menu.add_option('Random   Board', runGameOfLife)
    boards_menu.add_option('Back', pygameMenu.events.BACK)
    



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

        # Main menu
        main_menu.mainloop(events, disable_loop=test)



if __name__ == '__main__':
    main()
