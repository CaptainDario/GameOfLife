from tkinter import filedialog
import tkinter
import numpy as np
import tempfile
import os


def saveGrid(grid : [[]]):
    '''
    '''

    if(not os.path.isdir(os.path.join(tempfile.gettempdir(), 'gameOfLife'))):
        os.mkdir(os.path.join(tempfile.gettempdir(), 'gameOfLife'))

    np.save(os.path.join(tempfile.gettempdir(), 'gameOfLife', '1.npy'), grid)


def loadGrid(path : str):
    '''
    '''

    if(type(path) is tuple or
    not os.path.isfile(path)):
        print('Not a valid path!')
        return None

    loadedGrid = np.load(path, allow_pickle=True)
    #print(file)

    return loadedGrid

def openFileBrowser():
    '''
    '''

    root = tkinter.Tk()
    root.withdraw()
    selectedPath = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Game of Life files","*.npy"),("all files","*.*")))
    print(selectedPath)

    return selectedPath


def loadGridWithFileBrowser() -> [[]]:
    '''
    '''

    filePath = openFileBrowser()
    return loadGrid(filePath)

if __name__ == "__main__":
    #saveGrid(np.ones((10, 8), dtype=bool))
    #loadGrid(os.path.join(tempfile.gettempdir(), 'gameOfLife', '1.npy'))
    loadGridWithFileBrowser()