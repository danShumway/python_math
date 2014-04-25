class Menu():

    def __init__(self):
        #set up variables
        #python literally does not have private or hidden variables
        #but using __ will mangle them so they're hard to use/implied not to use
        self.options = [] #what the text for each menu item is
        self.optionsDelegates = [] #what functions it points to.
        self.currentlySelected = 0 #what menu item we're on.

#----------------------------------------------------------------------

    #Adds a new menu option.  We can handle this through a main game file or something.
    def addMenuItem(self, itemText, itemDelegate):
        self.options.append(itemText)
        self.optionsDelegates.append(itemDelegate)

#----------------------------------------------------------------------

    #select a menu item.
    def selectCurrent(self):
        self.optionsDelegates[self.currentlySelected]()
    
    
    

        

        
        
