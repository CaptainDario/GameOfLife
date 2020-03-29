from tkinter import filedialog
import tkinter
import numpy as np
import tempfile
import os


def saveGrid(grid : [[]], path : str, filename: str):
    '''
    '''

    if(not os.path.isdir(os.path.join(tempfile.gettempdir(), 'gameOfLife'))):
        os.mkdir(os.path.join(tempfile.gettempdir(), 'gameOfLife'))
    #print("path:",path)
    #print(filename)
    np.save(filename,grid.grid)
    #tempfile.gettempdir(), 'gameOfLife', 

def loadGrid(path : str):
    '''
    '''

    if(type(path) is tuple or
    not os.path.isfile(path)):
        print('Not a valid path!')
        return None

    loadedGrid = np.load(path, allow_pickle=True)
    print(loadedGrid)

    return loadedGrid

def openFileBrowser(save = False, filename = None):
    '''
    '''

    root = tkinter.Tk()
    root.withdraw()
    if(save == False):
        selectedPath = filedialog.askopenfilename(initialdir = "/",
                                                    title = "Select file",
                                                    filetypes = (("Game of Life files","*.npy"),("all files","*.*")))
        return selectedPath
    elif (save == True):
        if filename is None:
            filename = filedialog.asksaveasfilename(defaultextension=".npy")
            #print("Filename"+filename)
            #directory = os.path.split(filename)[0]
            return filename



def loadGridWithFileBrowser() -> [[]]:
    '''
    '''

    filePath = openFileBrowser()
    return loadGrid(filePath)

def saveGridWithFileBrowser(grid : [[]]):
    
      filename = openFileBrowser(True)
      filepath = os.path.split(filename)[0]
      #print(filepath)
      saveGrid(grid,filepath, filename )
      return 1



if __name__ == "__main__":
    #saveGrid(np.ones((10, 8), dtype=bool))
    #loadGrid(os.path.join(tempfile.gettempdir(), 'gameOfLife', '1.npy'))
    loadGridWithFileBrowser()