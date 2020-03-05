#!/bin/bash

#remove old executable
rm -R ./build/Linux

#build for linux
./gameOfLife/bin/pyinstaller --icon=./img/gameOfLife.ico --distpath=./build/Linux --name=GameOfLife --onefile ./src/main.py 

#remove tmp-files
rm -R ./build/GameOfLife
rm ./GameOfLife.spec
