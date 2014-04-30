import spyral
import snake

class Tile(spyral.Sprite):
    def __init__(self, scene, i, j,SIZE,key):
        super(Tile,self).__init__(scene)

        self.key = key
        self.anchor = 'center'
        self.type = 'empty'

        self.InitValues()

        self.row = i
        self.col = j

        self.x = (self.row*0.97) * self.image.width
        self.y = (self.col*0.97) * self.image.height

    def InitValues(self):
        if self.key == '#':
             self.image = spyral.Image('game/images/grassTile.png')
             self.type = 'empty'
        else:
             self.image = spyral.Image(size=(32,32)).fill((0,0,0))
             self.type = 'obstacle'


class Level(spyral.Scene):
    def __init__(self,SIZE):
        spyral.Scene.__init__(self, SIZE)
        self.background = spyral.Image(size=SIZE).fill((25,150,25))

        self.sceneSize = SIZE
        self.levelWidth = 20;
        self.levelHeight = 20;
        self.levelData = self.CreateLevel(SIZE,'game/levels/basic.txt')

        spyral.event.register("input.keyboard.down.*", self.handleKeyboard)

        #create snake player object
        self.player = snake.Snake(self, (5,12) )


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
                total = 0
                getWidth = True

                currentRow = 0
                currentCol = 0
                fileObject = open(filename)
                for line in fileObject:
                    line = line.rstrip('\n')
                    if getWidth == True:
                        self.levelWidth = len(line)
                        getWidth = False  
                    for char in line:
                        tile = Tile(self,currentCol,currentRow,SIZE,char)
                        level.append(tile)
                        currentCol += 1
                        if currentCol == self.levelWidth:
                            currentCol = 0
                            currentRow += 1
                    total += 1
                self.levelHeight = total
                fileObject.close()
            except:
                print('\nerror loading file!\n')
        return level

    def GetTile(self, row, column):
        return self.levelData[((row-1) * self.levelWidth) + (column-1)]

    def handleKeyboard(self, key):
        if unichr(key) == 'q':
            spyral.director.pop()
