# TABLE.PY

# Clases del motor
from engine.panel import Panel
import engine.graph as graph

# Clases utiles
from utils.vector2 import Vector2
from utils.print2d import Print2D as print2d

# Clases de la ui
from ui.textBox import TextBox

class Table:
    def __init__(self,title: str, colorId: int, margin: Vector2, cols: int, height = 0):
        self.height = height
        self.title = title
        self.colorId = colorId
        self.margin = margin.copy()
        self.cols = cols
        self._headings: list = []
        self._colors: dict = {
            "head" : [12 for x in range(self.cols)],
            "cont" : [12 for x in range(self.cols)]
        }
        self._sizes: dict = {
            "cols" : [8 for _ in range(self.cols)],
            "rows" : 3
        }
        self._content = []
        
    def setHeadings(self, *headings):
        if len(headings) >= self.cols:
            self._headings = [headings[x] for x in range(self.cols)]
        else:
            self._headings = ["null" for x in range(self.cols)]
            
    def setColors(self, headColor:list, contColor: list):
        self._colors["head"] = [
            headColor[x % len(headColor)]
            for x in range(self.cols)
        ]

        self._colors["cont"] = [
            contColor[x % len(contColor)]
            for x in range(self.cols)
        ]

    def addContet(self, *content):
        if len(content) >= self.cols:
            self._content.append([content[x] for x in range(self.cols)])
        else:
            self._content.append(["null" for x in range(self.cols)])
    
    def setColSize(self, value: list):
        self._sizes["cols"] = value
    
    def setRowSize(self, value):
        self._sizes["rows"] = value
        
    def clear(self):
        self._content = []
            
    def show(self):
        getStringSize = lambda string, x: (len(string) // x) + 1 if (len(string) % x > 0) else 1
        deltaSizeX = 0
        deltaSizeY = 0
        actualStringSize = 0
        theTextBox = TextBox(Vector2(1,1), Vector2(1,1), '', 12)
        chichis = 0
        
        for i in range(self.cols):
            theTextBox.position = Vector2(self.margin.x + deltaSizeX + 1, self.margin.y + deltaSizeY + 1)
            y = getStringSize(self._headings[i], self._sizes["cols"][i])
            if y > self._sizes["rows"]:
                y = self._sizes["rows"]
            elif y == 0:
                y = 1
            theTextBox.size = Vector2(self._sizes["cols"][i], y)
            theTextBox.content = self._headings[i]
            theTextBox.idColor = self._colors["head"][i]
            deltaSizeX += self._sizes["cols"][i]
            theTextBox.render()
            
            chichis = y if y > chichis else chichis
            
        deltaSizeY += chichis
        deltaSizeX = 0
        chichis = 0
        
        for i in range(len(self._content)):
            for j in range(self.cols):
                theTextBox.position = Vector2(self.margin.x + deltaSizeX + 1, self.margin.y + deltaSizeY + 1)
                y = getStringSize(self._content[i][j], self._sizes["cols"][j])
                if y > self._sizes["rows"]:
                    y = self._sizes["rows"]
                elif y == 0:
                    y = 1
                theTextBox.size = Vector2(self._sizes["cols"][j], y)
                theTextBox.content = self._content[i][j]
                theTextBox.idColor = self._colors["cont"][j]
                deltaSizeX += self._sizes["cols"][j]
                theTextBox.render()
                
                chichis = y if y > chichis else chichis
                
            deltaSizeY += chichis
            deltaSizeX = 0
            chichis = 0
            
        deltaSizeX = sum(self._sizes["cols"])
        
        if self.height > 0:
            deltaSizeY = self.height
        
        panel = Panel(self.title, self.colorId, self.margin - 1, Vector2(deltaSizeX, deltaSizeY))
        panel.render()
        
        
        
        
""""
Diagrama de como funciona
-------------------------
Obtiene la lista de encabezados
"""