import spyral
import copy
import random

headImage = spyral.Image('game/images/snakeHead.png')
bodyImage = spyral.Image('game/images/snakeBody.png')
tailImage = spyral.Image('game/images/snakeTail.png')

class Snake(object):
    def __init__(self, level, headPosition):
        self.x = headPosition[0]
        self.y = headPosition[1]
        self.level = level

        self.snakeTiles = []
        
        head = self.level.GetTile(headPosition[0],headPosition[1])
        head.image = headImage
        head.type = 'obstacle'
        self.snakeTiles.append(head)

        self.bodyLength = random.randint(1,2)
        for i in range(self.bodyLength):
            body = self.level.GetTile(self.x+i+1,self.y)
            body.image = bodyImage
            body.type = 'obstacle'
            self.snakeTiles.append(body)

        tail = self.level.GetTile(self.x+self.bodyLength+1,self.y)
        tail.image = tailImage
        tail.type = 'obstacle'

        self.snakeTiles.append(tail)

        spyral.event.register("input.keyboard.down.down", self.moveDown, scene=level)
        spyral.event.register("input.keyboard.down.up", self.moveUp, scene=level)
        spyral.event.register("input.keyboard.down.left", self.moveLeft, scene=level)
        spyral.event.register("input.keyboard.down.right", self.moveRight, scene=level)
	
    def ResetValues(self,headPosition):
        self.x = headPosition[0]
        self.y = headPosition[1]
        self.snakeTiles = []

        head = self.level.GetTile(headPosition[0],headPosition[1])
        head.image = headImage
        head.type = 'obstacle'
        self.snakeTiles.append(head)
        
        for i in range(self.bodyLength):
            body = self.level.GetTile(self.x+i+1,self.y)
            body.image = bodyImage
            body.type = 'obstacle'
            self.snakeTiles.append(body)

        tail = self.level.GetTile(self.x+self.bodyLength+1,self.y)
        tail.image = tailImage
        tail.type = 'obstacle'

        self.snakeTiles.append(tail)

    def handleKeyboard(self, key):
        if key == 276 or key == 260:
            self.moveLeft()
        elif key == 275 or key == 262:
            self.moveRight()
        elif key == 273 or key == 264:
            self.moveUp()
        elif key == 274 or key == 258:
            self.moveDown()

    def moveLeft(self, key):
        tileToInspect = self.level.GetTile(self.x,self.y - 1)
        if self.y - 1 > 0 and tileToInspect.type != 'obstacle':
            #let's check if you're moving onto an addition gate.
            #if(tileToInspect.type = 'add' and 
            self.y -= 1
            self.changeTilesFromMovement(tileToInspect);
               
    def moveRight(self, key):
        tileToInspect = self.level.GetTile(self.x,self.y + 1)
        if self.y + 1 <= self.level.levelWidth and tileToInspect.type != 'obstacle':
            self.y += 1
            self.changeTilesFromMovement(tileToInspect);

    def moveUp(self, key):
        tileToInspect = self.level.GetTile(self.x - 1,self.y)
        if self.x - 1 > 0 and tileToInspect.type != 'obstacle':
            self.x -= 1
            self.changeTilesFromMovement(tileToInspect);

    def moveDown(self, key):
        tileToInspect = self.level.GetTile(self.x + 1,self.y)
        if self.x + 1 <= self.level.levelHeight and tileToInspect.type != 'obstacle':
            self.x += 1
            self.changeTilesFromMovement(tileToInspect);

    def changeTilesFromMovement(self,tile):
        oldType = tile.type
        oldAmmount = tile.amount

        lipos = []
        li = []
        for i in self.snakeTiles:
            li.append(i.image)
            lipos.append( (i.row, i.col ) )

        self.snakeTiles[0] = self.level.GetTile(self.x,self.y)
        self.snakeTiles[0].image = headImage
        self.snakeTiles[0].type = 'obstacle'

        for i in range(len(self.snakeTiles)):
            if i >= 1:
                self.snakeTiles[i] = self.level.GetTile(lipos[i-1][1],lipos[i-1][0])
                self.snakeTiles[i].image = li[i]
                self.snakeTiles[i].type = 'obstacle'
        self.level.GetTile(lipos[len(lipos)-1][1],lipos[len(lipos)-1][0]).InitValues()

        if oldType == 'add':
            for i in range(oldAmmount):
                self.addTile()
        elif oldType == 'subtract':
            self.subtractTile(tile.amount)
        elif oldType == 'gate':
            self.level.goToNextLevel()

    def addTile(self):
        secondToLast = self.snakeTiles[len(self.snakeTiles)-2]
        tail = self.snakeTiles[len(self.snakeTiles)-1]

        directionX = secondToLast.col - tail.col
        directionY = secondToLast.row - tail.row

        self.snakeTiles[len(self.snakeTiles)-1] = self.level.GetTile(self.snakeTiles[len(self.snakeTiles)-1].col-directionX,self.snakeTiles[len(self.snakeTiles)-1].row-directionY)
        self.snakeTiles[len(self.snakeTiles)-1].image = tailImage

        newTile = self.level.GetTile(secondToLast.col-directionX,secondToLast.row-directionY)
        newTile.image = bodyImage
        self.snakeTiles.insert(len(self.snakeTiles)-1,newTile)

    def subtractTile(self, times=1):
        for i in range(times):
            #make sure the snake is never smaller than 3 tiles long
            if len(self.snakeTiles) >= 4:
                self.snakeTiles[len(self.snakeTiles)-1].InitValues()
                self.snakeTiles.pop()
                self.snakeTiles[len(self.snakeTiles)-1].image = tailImage
