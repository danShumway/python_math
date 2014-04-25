import spyral

class GameInput():

    def __init__(self):
        self.oldState = 0
        self.newState = 0
        self.currentKeys = []
        
        spyral.event.register("input.keyboard.up.*", self.SetCurrentKeyNone)

        spyral.event.register("input.keyboard.down.w", self.SetCurrentKeyW)
        spyral.event.register("input.keyboard.down.s", self.SetCurrentKeyS)
        spyral.event.register("input.keyboard.down.a", self.SetCurrentKeyA)
        spyral.event.register("input.keyboard.down.d", self.SetCurrentKeyD)

        spyral.event.register("input.keyboard.down.left", self.SetCurrentKeyLeft)
        spyral.event.register("input.keyboard.down.right", self.SetCurrentKeyRight)
        spyral.event.register("input.keyboard.down.up", self.SetCurrentKeyUp)
        spyral.event.register("input.keyboard.down.dowb", self.SetCurrentKeyDown)
        
    ##################################################################################
    #                               Set key functions                                #
    ##################################################################################
    def SetCurrentKeyNone(self):
        self.currentKeys = []
    def SetCurrentKeyW(self):
        self.currentKeys.append("w")
    def SetCurrentKeyS(self):
        self.currentKeys.append("s")
    def SetCurrentKeyA(self):
        self.currentKeys.append("a")
    def SetCurrentKeyD(self):
        self.currentKeys.append("d")
    def SetCurrentKeyLeft(self):
        self.currentKeys.append("left")
    def SetCurrentKeyRight(self):
        self.currentKeys.append("right")
    def SetCurrentKeyUp(self):
        self.currentKeys.append("up")
    def SetCurrentKeyDown(self):
        self.currentKeys.append("down")
    ##################################################################################
    ##################################################################################
    ##################################################################################
    
       
    def Update(self, deltaTime):
        self.oldState = self.newState

        if len(self.currentKeys) == 0:
            self.newState = 0
        else:
            self.newState = 1

    def IsKeyDown(self, key):
        if key in self.currentKeys:
            return True
        return False

    def IsKeyDownOnce(self, key):
        if self.oldState != self.newState and key in self.currentKeys:
            return True
        return False

        
        
