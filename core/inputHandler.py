from core.emitBus import bus
import core.states as states
import json
import msvcrt
from utils.print2d import Print2D as print2d

class Handlers:
    def __init__(self):
        self.handlers = {
            'draw' : {
                'up' : lambda: bus.emit('move-curse', 'u'),
                'down' : lambda: bus.emit('move-curse', 'd'),
                'left' : lambda: bus.emit('move-curse', 'l'),
                'right' : lambda: bus.emit('move-curse', 'r'),
                'accept' : lambda: bus.emit('draw-tile'),
                'cancel' : lambda: bus.emit('erase-tile'),
                'extra-0' : lambda: bus.emit('hide-curse'),
                'exit' : lambda: bus.emit('mp-stop'),
                'toogle': lambda: bus.emit('state-change', states.States.SELECTCOLOR),
                'alt-left': lambda: bus.emit('slct-tile', 'l'),
                'alt-right': lambda: bus.emit('slct-tile', 'r'),
                'extra-1': lambda: bus.emit('draw-clear'),
                'extra-2': lambda: bus.emit('fast-mode'),
                "toogle-2": lambda: bus.emit('state-change', states.States.LAYER)                                                                                 
            },
            'select' : {
                'toogle': lambda: bus.emit('state-change', states.States.DRAW),
                'exit' : lambda: bus.emit('mp-stop'),
                'up': lambda: bus.emit('slct-move', 'u'),
                'down': lambda: bus.emit('slct-move', 'd'),
                'left': lambda: bus.emit('slct-move', 'l'),
                'right': lambda: bus.emit('slct-move', 'r'),
                'extra-3': lambda: bus.emit('cstm-char'),
                'alt-left': lambda: bus.emit('slct-tile', 'l'),
                'alt-right': lambda: bus.emit('slct-tile', 'r'),
                'accept': lambda: bus.emit('slct-tile-change')
            },
            'layer' : {
                'up' : lambda: bus.emit('lyr-slct', 'u'),
                'down' : lambda: bus.emit('lyr-slct', 'd'),
                'left' : lambda: bus.emit('lyr-slct', 'l'),
                'right' : lambda: bus.emit('lyr-slct', 'r'),
                'toogle-2' : lambda: bus.emit('state-change', states.States.DRAW),
                'exit' : lambda: bus.emit('mp-stop'),
                'accept' : lambda: bus.emit('state-change', states.States.DRAW),
                'extra-3' : lambda: bus.emit('rnme-layer')
            }
        }
        
    def inputHandler(self):
        
        key = ''
        action = _kInput.get()
        bus.emit('clock-visible', False)
        match states.current:
            case states.States.DRAW:
                key = 'draw'
            case states.States.SELECTCOLOR:
                key = 'select'
            case states.States.LAYER:
                key = 'layer'
            
        if action in self.handlers[key]:
            self.handlers[key][action]()
        else:
            states.currentFlag = states.Flags.PASS
        bus.emit('clock-visible', True)
            
    def getKey(self, value: str = 'accept') -> str:
        for i, j in _kInput.inputMap.items():
            if j == value:
                return i

class Input:
    
    def __init__(self):
        #Esto es para la lectura del JSON
        self.inputMap = {}
        with open('data/inputMap.json', 'r') as inputMap:
            self.inputMap = json.load(inputMap)
        
    def get(self):
        try:
            action = msvcrt.getch().decode('utf-8').lower()
            if action in self.inputMap:
                return self.inputMap[action]
        except UnicodeDecodeError:
            pass
        
_kInput = Input()
kInput = Handlers()