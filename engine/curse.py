from core.emitBus import bus
from engine.tile import Tile
import engine.graph as graph
from utils.vector2 import Vector2
from utils.print2d import Print2D as print2d
from typing import Literal
import core.states as states

class Curse:
    def __init__(
        self,
        margin: Vector2 = Vector2(0,0),
        moveArea: Vector2 = Vector2(5,5),
        position: Vector2 = Vector2(1,1),
    ):
        self.margin = margin.copy()
        self.moveArea = moveArea.copy()
        self.position = position.copy()
        self.isVisible = True
        self.colorId = 12
        self.curse = '○'
        bus.conect('move-curse', self.move)
        bus.conect('hide-curse', self.hideNShow)
        
    def render(self):
        colorId = self.colorId
        if self.colorId == 15:
            colorId = 12
        
        if not self.isVisible:
            return
        
        print2d.coord(
            self.margin.x + self.position.x + 1,
            self.margin.y + self.position.y + 1,
            graph.ForeColors[colorId]['color'] + self.curse + graph.Reset.STYLE
        )
    
    def move(self, direction: Literal['u','d','l','r'] = 'r'):
        states.currentFlag = states.Flags.MOVE
        match direction:
            case 'u':
                self.position.y -= 1 if self.position.y > 1 else 0
            case 'd':
                self.position.y += 1 if self.position.y < self.moveArea.y else 0
            case 'l':
                self.position.x -= 1 if self.position.x > 1 else 0
            case 'r':
                self.position.x += 1 if self.position.x < self.moveArea.x else 0
    
    def hideNShow(self):
        self.isVisible = not self.isVisible
                