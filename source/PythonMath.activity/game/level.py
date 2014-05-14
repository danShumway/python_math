import spyral
import snake
import pythonMath
import random

################################################################################################################
#                                         Level text file key                                                  #
#                                                                                                              #
#   The first line in the file is the number the snake's length should be to progress through to the           #
#   next level                                                                                                 #
#                                                                                                              #
#   1 - 9: addition gate with the number being the amount added                                                #
#                                                                                                              #
#   p,o,i,u,y,t,l,k,j: subtraction gate                                                                        #
#                                                                                                              #
#   p : 1                                                                                                      #
#   o : 2                                                                                                      #
#   i : 3                                                                                                      #
#   u : 4                                                                                                      #
#   y : 5                                                                                                      #
#   t : 6                                                                                                      #
#   l : 7                                                                                                      #
#   k : 8                                                                                                      #
#   j : 9                                                                                                      #
#                                                                                                              #
#   # : obstacle (a bush for example)                                                                          #
#   - : blank tile                                                                                             #
#                                                                                                              #
################################################################################################################

subtractDict = { 'p': 1,
                 'o': 2,
                 'i': 3,
                 'u': 4,
                 'y': 5,
                 't': 6,
                 'l': 7,
                 'k': 8,
                 'j': 9 }

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

        self.image = tileBasic
        self.anchor = 'center'
        self.type = 'empty'

        self.amount = 1
        
        self.row = i
        self.col = j

        levelWidth = scene.levelWidth * self.image.width
        levelHeight = scene.levelHeight * self.image.height


        self.x = SIZE[0]/2 + ((self.row) * self.image.width) - levelWidth/2 + self.image.width
        self.y = SIZE[1]/2 + ((self.col) * self.image.height) - levelHeight/2

        self.InitValues()

    def InitValues(self):
        if self.key == '-':
             self.image = tileBasic
             self.type = 'empty'
             self.amount = 0
        elif self.key == '#':
             self.image = tileBush
             self.type = 'obstacle'
             self.amount = 0
        #addition gates
        elif self.key == '1' or self.key == '2' or self.key == '3' or self.key == '4' or self.key == '5' or self.key == '6' or self.key == '7' or self.key == '8' or self.key == '9':

             self.textSprite = spyral.Sprite(self.parent)
             text = spyral.Font("game/fonts/DejaVuSans.ttf", 22, (0,255,0) )
             self.textSprite.image = text.render(self.key)

             self.textSprite.x = self.x
             self.textSprite.y = self.y + 2
             self.textSprite.anchor = 'center'
            
             self.amount = int(self.key)
             self.image = tileAdd
             self.type = 'add'

             
        #subtraction gates
        elif self.key in subtractDict:

             self.textSprite = spyral.Sprite(self.parent)
             text = spyral.Font("game/fonts/DejaVuSans.ttf", 22, (255,0,0 ) )
             self.textSprite.image = text.render(str(subtractDict[self.key]))

             self.textSprite.x = self.x
             self.textSprite.y = self.y + 2
             self.textSprite.anchor = 'center'
            
             self.amount = subtractDict[self.key]
             self.image = tileSubtract
             self.type = 'subtract'
             
        #go to next level gate
        elif self.key == 'G':
             self.image = tileGate
             self.type = 'gate'
        #other
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
        self.goalAmount = 3
        self.startLength = 1
        
        self.levelData = self.CreateLevel(SIZE,filename)

        #create the text on the top of the screen that informs the player the length the snake needs
        #to be in order to progress to the next level
        self.hudGoalText = spyral.Sprite(self.parent)
        self.hudGoalStatus = spyral.Sprite(self.parent)
        self.text = spyral.Font("game/fonts/DejaVuSans.ttf", 22, (255,255,255 ) )
        self.hudGoalText.image = self.text.render("The snake needs to be " + str(self.goalAmount) + " pieces long to go to the next level!")

        self.hudGoalText.x = SIZE[0]/2
        self.hudGoalText.y = self.text.get_size("X").y
        self.hudGoalText.anchor = 'center'
        

        #create snake player object
        self.player = snake.Snake(self, (2,self.levelWidth/2) )

        spyral.event.register("input.keyboard.down.*", self.handleKeyboard, scene=self)


        self.hudGoalStatus.image = self.text.render("The snake is currently " + str(self.player.bodyLength) + " pieces long!")
        self.hudGoalStatus.x = SIZE[0]/2
        self.hudGoalStatus.y = self.text.get_size("X").y * 2.1
        self.hudGoalStatus.anchor = 'center'


    def CreateLevel(self, SIZE, filename = ''):
        level = {}
        #create from default width and height with no filename
        if filename == '':
            self.goalAmount = random.randint(3,10)
            for i in range(self.levelWidth):
                for j in range(self.levelHeight):
                    tile = Tile(self,i,j,SIZE,'-')
                    level[ (i, j) ] = tile
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
                    line = line.rstrip('\r')
                    if total == 0:
                        self.goalAmount = int(line)
                    elif total == 1:
                        self.startLength = int(line)
                    else:
                        if getWidth == True:
                            self.levelWidth = len(line)
                            getWidth = False  
                        for char in line:
                            tile = Tile(self,currentCol+1,currentRow+1,SIZE,char)
                            level[ (currentCol+1, currentRow+1) ] = tile
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
            return self.levelData[(column,row)]
        except:
            return None

    def handleKeyboard(self, key):
        if unichr(key) == 'q':
            spyral.director.pop()
        elif unichr(key) == 'r':
            self.restartLevel()

    def goToNextLevel(self):
        spyral.event.unregister("input.keyboard.down.*", self.handleKeyboard, scene=self)
        newLevel = Level(self.menuScene,self.sceneSize,'game/levels/level' + str(self.currentLevel + 1) + '.txt')
        newLevel.currentLevel = self.currentLevel + 1
        for key, value in self.levelData.iteritems():
            value.kill()
            del value
            self.levelData[key] = None
        for i in self.player.snakeTiles:
            i.kill()
            del i
        self.player.snakeTiles = []
        spyral.director.replace(newLevel)
        self.menuScene.theLevel = newLevel
        return
        
    def restartLevel(self):
        for key, value in self.levelData.iteritems():
            value.InitValues()
        self.player.ResetValues( (2,self.levelWidth/2) )
