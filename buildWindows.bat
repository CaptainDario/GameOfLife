::remove old executable
RMDIR /Q /S build\windows

::build for windows
pyinstaller --add-data .\music;music --add-data .\examples;examples --add-data .\fonts;pygameMenu\fonts --icon=.\img\gameOfLife.ico --distpath=.\build\windows --name=GameOfLife --noconsole  .\src\main.py

::remove tmp-files
RMDIR /Q /S build\GameOfLife
DEL /Q /S GameOfLife.spec
