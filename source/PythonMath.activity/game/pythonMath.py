import spyral
import random
import math
import level
import menu
import gameInput
from gameInput import InputClass

WIDTH = 1200
HEIGHT = 900
BG_COLOR = (0,255,0)
WHITE = (255, 255, 255)
SIZE = (WIDTH, HEIGHT)

class PythonMathGame(spyral.Scene):
    def __init__(self, *args, **kwargs):
        spyral.Scene.__init__(self, SIZE)
        self.background = spyral.Image(size=SIZE).fill(BG_COLOR)

        InputClass.RegisterEvents()

        self.MainMenuLogo = spyral.Sprite(self)
        logo_image = spyral.Image("game/logo.png")
        self.MainMenuLogo.image = logo_image

        self.MainMenuLogo.anchor = "center"

        self.MainMenuLogo.x = WIDTH/2
        self.MainMenuLogo.y = HEIGHT/2
        self.i = 0
        self.colorThing = (0, 0, 0)

        self.theLevel = level.Level()

        spyral.event.register("system.quit", spyral.director.pop)
        spyral.event.register("director.update", self.update)
        spyral.event.register("input.keyboard.down.q", spyral.director.pop)



        #some real stuff.  Still just hacking and testing, so not really really real.
        self.mainMenu = menu.Menu();
        self.mainMenu.addMenuItem("hello", self.moveSprite)
        self.currentlySelected = 0
        spyral.event.register("input.keyboard.down.a", self.mainMenu.selectCurrent)
        
        
    def update(self, delta):

        InputClass.Update(delta)

        #testing if update loop works.
        self.background = spyral.Image(size=SIZE).fill(self.colorThing)
        self.i += 1
        self.colorThing = (self.i, self.i, self.i)
        if(self.i == 250) :
            self.i = 0

        #This works as well
        #self.MainMenuLogo.x = self.MainMenuLogo.x + 1


        #To use the InputClass in other modules, type "import gameInput" and
        # "from gameInput import InputClass". You can then type InputClass.WHATEVER

        #This registers true only when the specified key was initially pressed
        #this is perfect for making sure a key does not "pulse"
        if InputClass.IsKeyDownOnce("w"):
            self.MainMenuLogo.y -= 2
        #This registers true whenever the key is pressed down
        if InputClass.IsKeyDown("s"):
            self.MainMenuLogo.y += 2


    def moveSprite(self):
        self.MainMenuLogo.x += 2
 
        
    
