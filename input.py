class Keyboard:
    class keys:
        KEY_A = 0
        KEY_B = 1
        KEY_SELECT = 2
        KEY_START = 3
        KEY_UP = 4
        KEY_DOWN = 5
        KEY_LEFT = 6
        KEY_RIGHT = 7
    
    def __init__(self, nes):
        self.nes = nes
        self.state1 = [0x40]*8
        self.state2 = [0x40]*8
    
    def setKey(self, value):
        pass #TODO:

