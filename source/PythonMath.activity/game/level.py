import spyral
import snake
import pythonMath

tileBasic = spyral.Image('game/images/grassTile.png')
tileBush = spyral.Image('game/images/bushTile.png')
tileAdd = spyral.Image('game/images/addTile.png')
tileSubtract = spyral.Image('game/images/subtractTile.png')
tileGate = spyral.Image('game/images/gateTile.png')
tileOther = spyral.Image(size=(32,32)).fill((0,0,0))

class Tile(spyral.Sprite):
    def __init__(self, scene, i, j,SIZE,key):
        super(Tile,self).__init__(scene)

        self.key = key
        self.anchor = 'center'
        self.type = 'empty'

        self.InitValues()

        self.row = i
        self.col = j

        levelWidth = scene.levelWidth * self.image.width
        levelHeight = scene.levelHeight * self.image.height

        self.x = SIZE[0]/2 + ((self.row*0.96) * self.image.width) - levelWidth/2 + self.image.width
        self.y = SIZE[1]/2 + ((self.col*0.96) * self.image.height) - levelHeight/2

    def InitValues(self):
        if self.key == '-':
             self.image = tileBasic
             self.type = 'empty'
        elif self.key == '#':
             self.image = tileBush
             self.type = 'obstacle'
        elif self.key == 'A':
             self.image = tileAdd
             self.type = 'add'
        elif self.key == 'S':
             self.image = tileSubtract
             self.type = 'subtract'
        elif self.key == 'G':
             self.image = tileGate
             self.type = 'gate'
        else:
             self.image = tileOther
             self.type = 'obstacle'


class Level(spyral.Scene):
    def __init__(self,menuScene,SIZE,filename):
        spyral.Scene.__init__(self, SIZE)
        self.background = spyral.Image(size=SIZE).fill((25,150,25))

        self.menuScene = menuScene
        self.sceneSize = SIZE
        self.levelWidth = 20;
        self.levelHeight = 20;

        self.currentLevel = 1
        
        self.levelData = self.CreateLevel(SIZE,filename)

        #create snake player object
        self.player = snake.Snake(self, (2,self.levelWidth/2) )

        spyral.event.register("input.keyboard.down.*", self.handleKeyboard)


    def CreateLevel(self, SIZE, filename = ''):
        level = []
        #create from default width and height with no filename
        if filename == '':
            for i in range(self.levelWidth):
                for j in range(self.levelHeight):
                    tile = Tile(self,i,j,SIZE,'-')
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
        try:
            return self.levelData[((row-1) * self.levelWidth) + (column-1)]
        except:
            return None

    def handleKeyboard(self, key):
        if unichr(key) == 'q':
            spyral.director.pop()
	elif unichr(key) == 'r':
	    self.restartLevel()

    def goToNextLevel(self):
        newLevel = Level(self.menuScene,self.sceneSize,'game/levels/level' + str(self.currentLevel + 1) + '.txt')
        newLevel.currentLevel = self.currentLevel + 1
        for i in self.levelData:
            i.kill()
            del i
        for i in self.player.snakeTiles:
            i.kill()
            del i
        spyral.director.replace(newLevel)
        self.menuScene.theLevel = newLevel
        return
		
    def restartLevel(self):
	for i in self.levelData:
	    i.InitValues()

	self.player.ResetValues( (2,self.levelWidth/2) )
