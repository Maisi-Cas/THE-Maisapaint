from core.emitBus import bus
from engine.tile import Tile
from engine.panel import Panel
import engine.graph as graph
from utils.vector2 import Vector2
from utils.print2d import Print2D as print2d
import core.states as states
from typing import Literal


class Layer:
    def __init__(self, margin: Vector2 = Vector2(0,0), size: Vector2 = Vector2(64,16)):
        self.margin = margin.copy()
        self.size = size.copy()
        self.pixels = {}
        bus.conect('draw-clear', self.clear)
        
    def addpixel(self, position: Vector2, tile: Tile):
        if position.x > self.size.x or position.y > self.size.y:
            return
        
        self.pixels[(position.x, position.y)] = (tile.foreColorId, tile.backColorId, tile.styleId, tile.character)
        
    def render(self):
        for (x,y),(a,b,c,d) in self.pixels.items():
            print2d.coord(
                x + self.margin.x,
                y + self.margin.y,
                (graph.ForeColors[a]['color'] + graph.BackColors[b]['color'] + graph.StyleType[c]['style'] + d + graph.Reset.STYLE)
            )
    
    def deletePixel(self, x, y):
        if (x, y) in self.pixels:
            del self.pixels[(x, y)]
            
    def clear(self):
        self.pixels = {}

class LayerMaster():
    def __init__(self, colorId: int, margin: Vector2, size: Vector2):
        self.tile = Tile(" ", 15, 15, 1)
        self.colorId = colorId
        self.margin = margin.copy()
        self.size = size.copy()
        if self.size.x < 3:
            self.size.x = 3
            
        self.layer: Layer
        self.layers: list[dict] = []
        for i in range(self.size.y):
            hatsuneMiku = {}
            hatsuneMiku["name"] = f"CAPA {i}"
            hatsuneMiku["enable"] = True
            hatsuneMiku["draw"] = {}
            self.layers.insert(0, hatsuneMiku)
        
        self.currentId = len(self.layers) - 1
        self.panel = Panel("Capas", self.colorId, self.margin - 1, self.size.copy())
        
        bus.conect("lyr-slct", self.select)

    def connect(self, layer: Layer):
        if isinstance(layer, Layer):
            self.layer = layer

    def select(self, direction: Literal['u', 'd', 'l', 'r'] = 'r'):
        states.currentFlag = states.Flags.CLAYER if direction in ['u', 'd'] else states.Flags.ULAYER
        
        match direction:
            case 'u':
                if self.currentId != 0:
                    self.currentId -= 1
                else:
                    self.currentId = len(self.layers) - 1
            
            case 'd':
                if self.currentId != len(self.layers) - 1:
                    self.currentId += 1
                else:
                    self.currentId = 0
            case 'l': 
                self.layers[self.currentId]["enable"] = not self.layers[self.currentId]["enable"]
            case 'r': 
                self.layers[self.currentId]["enable"] = not self.layers[self.currentId]["enable"]
        
    def count(self, index):
        counter = {
            "char" : {},
            "fore" : {},
            "back" : {},
            "style" : {}
        }
        
        if len(self.layers[index]["draw"].values()) == 0:
            return  [" ", 15, 15, 1]
        
        for draw in self.layers[index]["draw"].values():
            char = draw[3]
            counter["char"][char] = counter["char"].get(char, 0) + 1
            fore = draw[0]
            counter["fore"][fore] = counter["fore"].get(fore, 0) + 1
            back = draw[1]
            counter["back"][back] = counter["back"].get(back, 0) + 1
            style = draw[2]
            counter["style"][style] = counter["style"].get(style, 0) + 1
        
        tile = [
            max(counter["char"], key=counter["char"].get),
            max(counter["fore"], key=counter["fore"].get),
            max(counter["back"], key=counter["back"].get),
            max(counter["style"], key=counter["style"].get)
        ]
            
        return tile
    
    def render(self):
        self.panel.render(True)
        colors = {
            'd' : 14,
            'e' : 12
        }
        ses : str = ''
        key: int
        
        for i in range(len(self.layers)):
            kasaneTeto = 0
            
            if i == self.currentId:
                ses = graph.BackColors[self.colorId]['color']
                if states.current == states.States.LAYER:
                    kasaneTeto = 1
            
            if self.layers[i]["enable"]:
                key = colors["e"]
            else:
                key = colors["d"]
            tile = self.count(i)
            self.tile.character, self.tile.foreColorId, self.tile.backColorId, self.tile.styleId = tile[0], tile[1], tile[2], tile[3]
            print2d.coord(self.margin.x + 1, self.margin.y + 1 + i, ses + (" " * self.size.x) + graph.Reset.STYLE)
            print2d.coord(self.margin.x + 1 + kasaneTeto, self.margin.y + 1 + i, graph.ForeColors[key]["color"] + f"[{self.tile}{graph.ForeColors[key]["color"]}]{ses}[{self.layers[i]["name"][:self.size.x - (3 + kasaneTeto + 2)]}]{graph.Reset.STYLE}")
            ses = ''
            
    def renderDraws(self):
        # Este codigo en honor a Maxi
        self.layer.pixels.clear()
        
        for i in range(len(self.layers) - 1, -1, -1):
            if len(self.layers[i]["draw"]) > 0 and self.layers[i]["enable"]:
                for (x, y), (a,b,c,d) in self.layers[i]["draw"].items():
                    self.layer.pixels[(x, y)] = (a, b, c, d)
                    
        self.layer.render()
    
    def addpixel(self, position: Vector2, tile: Tile):
        if self.layers[self.currentId]["enable"]:
            self.layers[self.currentId]["draw"][(position.x, position.y)] = (tile.foreColorId, tile.backColorId, tile.styleId, tile.character)
    
    def deletePixel(self, x, y):
        if (x, y) in self.layers[self.currentId]["draw"]:
            del self.layers[self.currentId]["draw"][(x, y)]
            
    def clear(self):
        self.layers[self.currentId]["draw"] = {}
        
        