from utils.vector2 import Vector2
from utils.print2d import Print2D as print2d
import engine.graph as graph
from engine.panel import Panel
from engine.tile import Tile
from typing import Literal
from core.emitBus import bus
import random as rand
import core.states as states
from utils.sound import Audio

class TileSelector:
    def __init__(self, position: Vector2, count: int):
        self.position = position
        self.count: int
        if count > 0:
            if count <= len(graph.Characters):
                self.count = count
            else:
                self.count = len(graph.Characters)
        else:
            self.count = 1
            
        self.currenTile = 0
        self.tiles = []
        for i in range(self.count):
            isFore = bool(rand.randint(0,1))
            self.tiles.append(
                Tile(
                    graph.Characters[rand.randint(0,len(graph.Characters) - 1)]["character"],
                    (i % len(graph.ForeColors) if isFore else 15),
                    (i % len(graph.BackColors) if not isFore else 15),
                    1
                )
            )
        self.panel = Panel(
            'Selector de Tiles',
            self.tiles[self.currenTile].foreColorId,
            self.position - 2,
            Vector2(self.count * 3, 1)
        )
        bus.conect('slct-tile', self.moveTile)
        
        
    def render(self):
        self.panel.colorId = self.tiles[self.currenTile].foreColorId
        
        if self.panel.colorId == 15:
            self.panel.colorId = 12
        
        for i in range(self.count):
            print2d.coord(self.position.x + (i * 3), self.position.y, f"[{self.tiles[i]}]")
        
        if self.currenTile < len(self.tiles) // 2:
            self.panel.indent = (self.panel.size.x // 2) + ((self.panel.size.x // 2) - len(self.panel.title))
        else:
            self.panel.indent = 2
        self.panel.render()
        print2d.coord(self.position.x + (self.currenTile * 3) + 1, self.position.y - 1, graph.ForeColors[self.panel.colorId]['color'] + '▼' + graph.Reset.STYLE)
        print2d.coord(self.position.x + (self.currenTile * 3) + 1, self.position.y + 1, graph.ForeColors[self.panel.colorId]['color'] + '▲' + graph.Reset.STYLE)
    
    def change(self, characterId: int, foreColorId: int, backColorId: int, styleId: int):
        self.tiles[self.currenTile] = Tile(characterId, foreColorId, backColorId, styleId)
        
    def moveTile(self, direction: Literal['l','r'] = 'r'):
        states.currentFlag = states.Flags.CTILE
        match direction:
            case 'l':
                if self.currenTile != 0:
                    self.currenTile -= 1
                else:
                    self.currenTile = len(self.tiles) - 1
            case 'r':
                if self.currenTile != len(self.tiles) - 1:
                    self.currenTile += 1
                else:
                    self.currenTile = 0
            case _:
                pass