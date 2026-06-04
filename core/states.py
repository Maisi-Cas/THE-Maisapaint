from enum import Enum

class States(Enum):
    DRAW = 0
    SELECTCOLOR = 1
    LAYER = 2

class Flags(Enum):
    NONE = 0
    DRAW = 1
    MOVE = 2
    SELECTION = 3
    PASS = 4
    CTILE = 5
    CLAYER = 6
    ULAYER = 7

currentFlag = Flags.NONE
current = States.DRAW 

isRendering:bool = True
clockIsRendering:bool = False
isMsgBoxOn: bool = False