import spyral

class Tile(spyral.Sprite):
    def __init__(self, scene, i, j,SIZE):
        super(Tile,self).__init__(scene)

        self.image = spyral.Image('game/grassTile.png')
        self.anchor = 'center'

        self.x = i * self.image.width + SIZE[0]/4
        self.y = j * self.image.height + SIZE[1]/4

        
class Level(spyral.Scene):
    def __init__(self,SIZE):
        spyral.Scene.__init__(self, SIZE)
        self.background = spyral.Image(size=SIZE).fill((75,255,75))
        
        #set up variables
        self.levelWidth = 20;
        self.levelHeight = 20;
        self.levelData = self.CreateLevel(self.levelWidth, self.levelHeight,SIZE)

        spyral.event.register("director.update", self.update)
        spyral.event.register("input.keyboard.down.q", spyral.director.pop)

    #makes a blank world and returns it.
    #Todo: load in worlds from external files.
    def CreateLevel(self, width, height,SIZE):
        level = []
        for i in range(width):
            for j in range(height):
                tile = Tile(self,i,j,SIZE)
                level.append(tile)
        return level

    def update(self, delta):
        pass
