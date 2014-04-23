import spyral
import random
import math

WIDTH = 1200
HEIGHT = 900
BG_COLOR = (0,255,0)
WHITE = (255, 255, 255)
SIZE = (WIDTH, HEIGHT)

class PythonMathGame(spyral.Scene):
    def __init__(self, *args, **kwargs):
        spyral.Scene.__init__(self, SIZE)
        self.background = spyral.Image(size=SIZE).fill(BG_COLOR)

        self.MainMenuLogo = spyral.Sprite(self)
        logo_image = spyral.Image("game/logo.png")
        self.MainMenuLogo.image = logo_image

        self.MainMenuLogo.anchor = "center"

        self.MainMenuLogo.pos.x = WIDTH/2
        self.MainMenuLogo.pos.y = HEIGHT/2

        spyral.event.register("system.quit", spyral.director.pop)
        spyral.event.register("director.update", self.update)
        spyral.event.register("input.keyboard.down.q", spyral.director.pop)
        
    def update(self, delta):
        pass
    
