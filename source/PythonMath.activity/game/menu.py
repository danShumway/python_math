import spyral
import math
import random

class Menu():

    def __init__(self, scene):
        #set up variables
        #python literally does not have private or hidden variables, as far as I know.
        self.parentScene = scene #A reference to the drawy part.
        self.options = [] #what the text for each menu item is
        self.optionsDelegates = [] #what functions it points to.
        self.currentlySelected = 0 #what menu item we're on.
        self.sprites = [] #Our sprites.
        self.width = 0
        self.height = 0 #width and height of the entire menu
        self.originX = 0
        self.originY = 0

#----------------------------------------------------------------------

    #Adds a new menu option.  We can handle this through a main game file or something.
    def addMenuItem(self, itemText, itemDelegate):
        self.options.append(itemText)
        self.optionsDelegates.append(itemDelegate)
        #add the actual sprite.  These are drawn automatically on the scene that's passed in.
        #there is no draw loop.
        option = spyral.Sprite(self.parentScene)
        self.sprites.append(option)
        option.image = spyral.Image("game/logo.png")
        #recalculate the position of everything on the screen.
        option.anchor = "center"
        #option.width = 100
        #option.height = 100
        option.x = self.width/2 # + self.originX
        option.y = self.height/2 # + self.originY
        print(self.width/2)
        print(option.x)
        
#----------------------------------------------------------------------

    #select a menu item.
    def selectCurrent(self):
        self.optionsDelegates[self.currentlySelected]()
        #highlight the selected option.

    def moveUp(self):
        self.currentlySelected = (self.currentlySelected - 1) % len(self.options)

    def moveDown(self):
        self.currentlySelected = (self.currentlySelected + 1) % len(self.options)
    
    
    

        

        
        
