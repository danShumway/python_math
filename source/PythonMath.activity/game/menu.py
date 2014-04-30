import spyral
import math
import random

class Menu():

    def __init__(self, scene, width, height):
        #set up variables
        #python literally does not have private or hidden variables, as far as I know.
        self.parentScene = scene #A reference to the drawy part.
        self.options = [] #what the text for each menu item is
        self.optionsDelegates = [] #what functions it points to.
        self.currentlySelected = 0 #what menu item we're on.
        self.sprites = [] #Our sprites.
        self.width = width
        self.height = height #width and height of the entire menu

        spyral.event.register("input.keyboard.down.up", self.moveUp)
        spyral.event.register("input.keyboard.down.down", self.moveDown)
        
#----------------------------------------------------------------------

    #Adds a new menu option.  We can handle this through a main game file or something.
    def addMenuItem(self, itemText, itemDelegate):
        self.options.append(itemText)
        self.optionsDelegates.append(itemDelegate)
        #add the actual sprite.  These are drawn automatically on the scene that's passed in.
        #there is no draw loop.
        option = spyral.Sprite(self.parentScene)
        self.sprites.append(option)

        #quick check if you added only 1 item.
        if(len(self.options) != 1):
            option.image = spyral.Image("game/images/logo.png")
        else:
            option.image = spyral.Image("game/images/selectedMenuItem.png")
            
        #recalculate the position of everything on the screen.
        option.anchor = "center"
        option.x = self.width/2

        #fix positions.
        print("Length: " + str(self.height/2))
        curY = self.height/2 - ((len(self.options) - 1 )* self.sprites[0].height/2)
        for i in range(0, len(self.sprites)):
            print("CurY: " + str(curY))
            self.sprites[i].y = curY
            curY = curY + self.sprites[i].height + 30
        
#----------------------------------------------------------------------

    #select a menu item.
    def selectCurrent(self):
        self.optionsDelegates[self.currentlySelected]()
        #highlight the selected option.

    def moveUp(self):
        self.sprites[self.currentlySelected].image = spyral.Image("game/images/logo.png")
        self.currentlySelected = (self.currentlySelected - 1) % len(self.options)
        self.sprites[self.currentlySelected].image = spyral.Image("game/images/selectedMenuItem.png")

    def moveDown(self):
        self.sprites[self.currentlySelected].image = spyral.Image("game/images/logo.png")
        self.currentlySelected = (self.currentlySelected + 1) % len(self.options)
        self.sprites[self.currentlySelected].image = spyral.Image("game/images/selectedMenuItem.png")
    
    
    

        

        
        
