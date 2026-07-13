import engine.graph as graph
from utils.vector2 import Vector2
from utils.print2d import Print2D as print2d

class Panel:
    def __init__(self, title: str, colorId: int, margin: Vector2, size: Vector2, indent = 2):
        self.title = title
        self.colorId = colorId
        self.margin = margin.copy()
        self.size = size.copy()
        self.indent = indent
        self.subTitleIndent = 2
        self.subTitle = ''
        self.type = 'normal'
        
    def render(self, clear: bool = False):
        borders = {
            'normal' : '┌┐└┘─│',
            'double' : '╔╗╚╝═║'
        }
        title = ''
        if len(self.subTitle) > 0:
            title = self.title + f'{graph.ForeColors[self.colorId]['color']}{borders[self.type][4] * self.subTitleIndent}[{self.subTitle}{graph.ForeColors[self.colorId]['color']}]'
        else:
            title = self.title
        # Aplicamos color
        print(graph.ForeColors[self.colorId]['color'])
        
        if not self.type in borders.keys():
            self.type = 'normal'
        
        # Comenzamos a imprimir las esquinas
        
        print2d.coord(
            self.margin.x + 1,
            self.margin.y + 1,
            borders[self.type][0]
        )
        print2d.coord(
            self.margin.x + self.size.x + 2,
            self.margin.y + 1,
            borders[self.type][1]
        )
        print2d.coord(
            self.margin.x + 1,
            self.margin.y + self.size.y + 2,
            borders[self.type][2]
        )
        print2d.coord(
            self.margin.x + self.size.x + 2,
            self.margin.y + self.size.y + 2,
            borders[self.type][3]
        )
        print2d.coord(
            self.margin.x + 2,
            self.margin.y + 1,
            borders[self.type][4] * self.size.x
        )
        print2d.coord(
            self.margin.x + 2,
            self.margin.y + self.size.y + 2,
            borders[self.type][4] * self.size.x
        )
            
        for i in range(self.size.y):
            print2d.coord(
                self.margin.x + 1,
                self.margin.y + 2 + i,
                borders[self.type][5]
            )
            print2d.coord(
                self.margin.x + self.size.x + 2,
                self.margin.y + 2 + i,
                borders[self.type][5]
            )
        print2d.coord(
            self.margin.x + 1 + self.indent,
            self.margin.y + 1,
            title
        )
        print(graph.Reset.STYLE)
        
        if clear:
            fillString = ' ' * self.size.x
            for i in range(self.size.y):
                print2d.coord(self.margin.x + 2, self.margin.y + 2 + i, fillString)
    