class Level():

    #constructor
    def __init__(self):
        #set up variables
        self.levelWidth = 20;
        self.levelHeight = 20;
        self.level = self.defineBlankWorld(self.levelWidth, self.levelHeight)
        

#-------------------------------------------------------------------------
        

    #makes a blank world and returns it.
    #Todo: load in worlds from external files.
    def defineBlankWorld(self, width, height):
        level = [[0]*width for i in range(height)]
        #makes a new level to return.
        for x in xrange(0, width):
            for y in xrange(0, height):
                #make walls
                if(x == 0 or x == width - 1 or y == 0 or y == height - 1):
                    level[x][y] = 1;
                else:
                    level[x][y] = 0;
        return level

#-------------------------------------------------------------------------

    def draw(self, x, y, width, height):
        pass
    
    def otherStuff(self):
        pass
        
