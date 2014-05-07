import spyral
import pygame

import sys
import os
import random
import math
import level
import menu

WIDTH = 1200
HEIGHT = 900
SIZE = (WIDTH, HEIGHT)

class PythonMathGame(spyral.Scene):
    def __init__(self, *args, **kwargs):
        spyral.Scene.__init__(self, SIZE)
        self.background = spyral.Image(size=SIZE).fill((0,0,0))

        self.theLevel = level.Level(self,SIZE,'game/levels/tinyLevel.txt')

        self.mainMenu = menu.Menu(self, WIDTH, HEIGHT)
        self.mainMenu.addMenuItem('Play', self.startLevel)
        self.mainMenu.addMenuItem('Filler', self.startLevel)
        self.mainMenu.addMenuItem('Quit', sys.exit)

        spyral.event.register("input.keyboard.down.*", self.handleKeyboard)
        spyral.event.register("director.update", self.update)
        spyral.event.register("system.quit", sys.exit)
        

    def handleKeyboard(self, key):   
        if unichr(key) == 'e':
            spyral.director.push(self.theLevel)
        elif unichr(key) == 'q':
            spyral.director.pop()
        elif unichr(key) == 'a':
            self.mainMenu.selectCurrent()
        elif unichr(key) == ' ':
            self.mainMenu.selectCurrent()

    def update(self, delta):
        pass
    
    def startLevel(self):
        spyral.director.push(self.theLevel)

    
