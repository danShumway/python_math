import spyral
import gameInput
from gameInput import InputClass

class Tile(spyral.Sprite):
    def __init__(self, scene, i, j,SIZE,key):
        super(Tile,self).__init__(scene)

        if key == '#':
             self.image = spyral.Image('game/grassTile.png')
        else:
             self.image = spyral.Image(size=(32,32)).fill((0,0,0))
        self.anchor = 'center'

        self.x = (i*0.95) * self.image.width + SIZE[0]/2 - (scene.levelWidth/2 * self.image.width)
        self.y = (j*0.95) * self.image.height + SIZE[1]/2 - (scene.levelWidth/2 * self.image.height)


class Level(spyral.Scene):
    def __init__(self,SIZE):
        spyral.Scene.__init__(self, SIZE)
        self.background = spyral.Image(size=SIZE).fill((25,150,25))

        self.sceneSize = SIZE
        self.levelWidth = 20;
        self.levelHeight = 20;
        self.levelData = self.CreateLevel(SIZE,'game/level.txt')

        spyral.event.register("director.update", self.update)
        spyral.event.register("input.keyboard.down.q", spyral.director.pop)

        InputClass.RegisterEvents()

    #makes a blank world and returns it.
    #Todo: load in worlds from external files.
    def CreateLevel(self, SIZE, filename = ''):
        level = []
        #create from default width and height with no filename
        if filename == '':
            for i in range(self.levelWidth):
                for j in range(self.levelHeight):
                    tile = Tile(self,i,j,SIZE,'#')
                    level.append(tile)
        #create from file
        else:
            try:
                fileObject = open(filename,'r')
                fileData = fileObject.read()

                count = 0
                setWidth = True
                for i in fileData:
                    if i == '\n':
                        if setWidth == True:
                            self.levelWidth = count
                            setWidth = False
                    count+=1
                self.levelHeight = count / self.levelWidth   
                fileObject.close()

                currentRow = 0
                currentCol = 0
                for i in range(self.levelWidth * self.levelHeight):
                    if fileData[i] != '\n':
                        tile = Tile(self,currentCol,currentRow,SIZE,fileData[i])
                        level.append(tile)
                        currentCol += 1
                        if currentCol == self.levelWidth:
                            currentCol = 0
                            currentRow += 1
            except:
                print('file not found!')
        return level

    def update(self, delta):
        InputClass.Update(delta)
        self.PanCamera()

    def GetTile(self, row, column):
        return self.levelData[((row-1) * self.levelWidth) + (column-1)]

    def PanCamera(self):
        xOffset = 0
        yOffset = 0
        if InputClass.mouseData.x <= 15:
            xOffset = 3
        elif InputClass.mouseData.x >= self.sceneSize[0] - 15:
            xOffset = -3
        if InputClass.mouseData.y <= 15:
            yOffset = 3
        elif InputClass.mouseData.y >= self.sceneSize[1] - 15:
            yOffset = -3
        if yOffset != 0 or xOffset != 0:
            for i in self.levelData:
                i.x += xOffset
                i.y += yOffset
