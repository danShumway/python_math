import spyral
import copy
import random

class Snake(object):
    def __init__(self, level, headPosition):
        self.x = headPosition[0]
        self.y = headPosition[1]
        self.level = level

        self.snakeTiles = []
        
        head = self.level.GetTile(headPosition[0],headPosition[1])
        head.image = spyral.Image('game/images/snakeHead.png')
        head.type = 'obstacle'
        self.snakeTiles.append(head)

        bodyLength = random.randint(1,6)
        for i in range(bodyLength):
            body = self.level.GetTile(self.x+i+1,self.y)
            body.image = spyral.Image('game/images/snakeBody.png')
            body.type = 'obstacle'
            self.snakeTiles.append(body)

        tail = self.level.GetTile(self.x+bodyLength+1,self.y)
        tail.image = spyral.Image('game/images/snakeTail.png')
        tail.type = 'obstacle'

        self.snakeTiles.append(tail)

        spyral.event.register("input.keyboard.down.left", self.moveLeft)
        spyral.event.register("input.keyboard.down.right", self.moveRight)
        spyral.event.register("input.keyboard.down.up", self.moveUp)
        spyral.event.register("input.keyboard.down.down", self.moveDown) 

    def moveLeft(self):
        if self.y - 1 > 0 and self.level.GetTile(self.x,self.y - 1).type != 'obstacle':
            self.y -= 1
            self.changeTilesFromMovement();
               
    def moveRight(self):
        if self.y + 1 <= self.level.levelWidth and self.level.GetTile(self.x,self.y + 1).type != 'obstacle':
            self.y += 1
            self.changeTilesFromMovement();

    def moveUp(self):
        if self.x - 1 > 0 and self.level.GetTile(self.x - 1,self.y).type != 'obstacle':
            self.x -= 1
            self.changeTilesFromMovement();

    def moveDown(self):
        if self.x + 1 < self.level.levelHeight and self.level.GetTile(self.x + 1,self.y).type != 'obstacle':
            self.x += 1
            self.changeTilesFromMovement();
    
    def changeTilesFromMovement(self):
        lipos = []
        li = []
        for i in self.snakeTiles:
            li.append(i.image)
            lipos.append( (i.row, i.col ) )

        self.snakeTiles[0] = self.level.GetTile(self.x,self.y)
        self.snakeTiles[0].image = spyral.Image('game/images/snakeHead.png')
        self.snakeTiles[0].type = 'obstacle'

        for i in range(len(self.snakeTiles)):
            if i >= 1:
                self.snakeTiles[i] = self.level.GetTile(lipos[i-1][1]+1,lipos[i-1][0]+1)
                self.snakeTiles[i].image = li[i]
                self.snakeTiles[i].type = 'obstacle'

        self.level.GetTile(lipos[len(lipos)-1][1]+1,lipos[len(lipos)-1][0]+1).InitValues()
        
