##################################################################################################################
#
#  Game Input class - Contains the class itself under the InputClass variable.
#  To use it in a script type "import gameInput", and then "from gameInput import
#  InputClass"
#
#
#  IsKeyDown and IsKeyDownOnce methods: returns true if the specified key
#                                       is currently pressed down (The once
#                                       method will prevent keyboard pulsing)
#
#  Example:    InputClass.IsKeyDown('w') - returns true if the w key is pressed down
#
#
#
#  IsButtonDown and IsButtonDownOnce methods: returns true if the specified mouse button
#                                             is currently pressed down (The once
#                                             method will prevent button pulsing)
#
#
#  Example:    InputClass.IsButtonDown('left') - returns true if the left mouse button is pressed down
#
##################################################################################################################

import spyral

keyDict = { 119 : 'w',
            115 : 's',
            97 : 'a',
            100 : 'd',
            273 : 'up',
            274 : 'down',
            276 : 'left',
            275 : 'right',
            101 : 'e',
            114 : 'r',
            116 : 't',
            121 : 'y',
            117 : 'u',
            105 : 'i',
            111 : 'o',
            112 : 'p',
            102 : 'f',
            103 : 'g',
            104 : 'h',
            106 : 'j',
            107 : 'k',
            108 : 'l',
            122 : 'z',
            120 : 'x',
            99 : 'c',
            118 : 'v',
            98 : 'b',
            110 : 'n',
            109 : 'm',
            
            49 : '1',
            50 : '2',
            51 : '3',
            52 : '4',
            53 : '5',
            54 : '6',
            55 : '7',
            56 : '8',
            57 : '9',
            48 : '0'}

class MouseData(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.changeX = 0
        self.changeY = 0
        self.buttonStatus = []
        self.rect = spyral.Rect(0,0,2,2)

        self.oldState = 0
        self.newState = 0

    #Prints info about the mouse
    def Print(self):
        print('\nX: ' + str(self.x) + '\nY: ' + str(self.y) + '\nChangeX: ' + str(self.changeX) + '\nChangeY: ' + str(self.changeY))
        print('Current mouse buttons pressed: ')
        print(self.buttonStatus)

    def Update(self, deltaTime):
        self.oldState = self.newState
        self.rect = spyral.Rect(self.x,self.y,2,2)
        if len(self.buttonStatus) == 0:
            self.newState = 0
        else:
            self.newState = 1         

    #Returns true if the specified mouse button is pressed down
    def IsButtonDown(self, button):
        if button in self.buttonStatus:
            return True
        return False
    
    #Returns true if the specified mouse button is pressed down. Will prevent pulsing of the event
    def IsButtonDownOnce(self, button):
        if self.oldState != self.newState and button in self.buttonStatus:
            return True
        return False

        
class GameInput(object):

    def __init__(self):
        self.oldState = 0
        self.newState = 0
        self.currentKeys = []

        self.mouseData = MouseData()
        
    def RegisterEvents(self):
        
        #Keyboard events
        spyral.event.register("input.keyboard.up", self.SetCurrentKeyNone)
        spyral.event.register("input.keyboard.down", self.SetCurrentKey)
        
        #Mouse events
        spyral.event.register("input.mouse.motion", self.HandleMouseMotion)
       
    ##################################################################################
    #                               Set key functions                                #
    ##################################################################################

    #Keyboard
    def SetCurrentKeyNone(self):
        self.currentKeys = []
    def SetCurrentKey(self, key, mod):
        if key in keyDict:
            self.currentKeys.append(keyDict[key])

    #Mouse
    def HandleMouseMotion(self, pos, rel, buttons, left, right, middle):
        self.mouseData.buttonStatus = []
        self.mouseData.x = pos[0]
        self.mouseData.y = pos[1]
        self.mouseData.changeX = rel[0]
        self.mouseData.changeY = rel[1]

        if left == True:
            self.mouseData.buttonStatus.append('left')
        if middle == True:
            self.mouseData.buttonStatus.append('middle')
        if right == True:
            self.mouseData.buttonStatus.append('right')

        
    ##################################################################################
    ##################################################################################
    ##################################################################################
    
       
    def Update(self, deltaTime):
        self.mouseData.Update(deltaTime)
        self.oldState = self.newState

        if len(self.currentKeys) == 0:
            self.newState = 0
        else:
            self.newState = 1

    #Returns true if the specified key is pressed down
    def IsKeyDown(self, key):
        if key in self.currentKeys:
            return True
        return False

    #Returns true if the specified key is pressed down. Will prevent pulsing of the event
    def IsKeyDownOnce(self, key):
        if self.oldState != self.newState and key in self.currentKeys:
            return True
        return False

# The actual input class variable used throughout the game. This is important. Be sure to use this specific variable and do not make a
# new class of this type. To use this specific variable in any python file, type:
#
# import gameInput
# from gameInput import InputClass
#
# then use InputClass as a variable. For example: InputClass.IsKeyDown('w')
#
InputClass = GameInput()
