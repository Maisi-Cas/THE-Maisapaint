# Clases utiles
from utils.vector2 import Vector2
from utils.print2d import Print2D

# Clases del motor
from engine.panel import Panel
import engine.graph as graph

# Clases del nucleo
import core.states as states
from core.inputHandler import kInput

# Clases de python
import random as rand
import time
import msvcrt
from enum import Enum

class Menu:

    class RenderState(Enum):

        OPTIONS = 0
        ALL = 1

    canRender = True
    isOpen = True
    OPTIONNAMES = [
        {"color" : 2, "name": "Volver", "icon" : ">"},
        {"color" : 0, "name": "Salir", "icon" : "<"},
        {"color": 10, "name": "Nuevo Dibujo", "icon" : "+"},
        {"color" : 6, "name": "Cargar", "icon" : "^"},
        {"color" : 4, "name": "Guardar", "icon" : "v"}
    ]

    def __init__(self, position: Vector2, colorId: int, msp):
        self.currentRState = self.RenderState.ALL
        self.PYTHONCONCACA = 4
        self.msp = msp
        self.currentId = 0
        self.position = position.copy()
        self.colorId = colorId
        self.mainPanel = Panel(

            "MENU",
            self.colorId,
            self.position.copy(),
            Vector2(
                32,
                (len(self.OPTIONNAMES) * 2) + 3
            )
            
        )

    def renderOptions(self):
        suco = lambda niggas, index : "-----" if self.currentId != index else (">>>>>" if niggas else "<<<<<") 
        sucoII = lambda index : self.OPTIONNAMES[index]["name"].lower() if index != self.currentId else self.OPTIONNAMES[index]["name"].upper()
        sucoIII = lambda index, trans : (" <" if trans else "> ") if index == self.currentId else ""
        sucoIV = lambda index : 1 if index == self.currentId else 0
        sucoV = lambda e: f"{graph.foreColor(e) if rand.randint(0, 4) < 4 else graph.foreColor(rand.randint(0,14))}{graph.style(0)}{graph.character(rand.randint(0, len(graph.Characters) - 1))}{graph.Reset.STYLE}" 

        for i in range(0, len(self.OPTIONNAMES)):
            if i == self.currentId:
                Print2D.coord(
                    self.position.x + 5,
                    self.position.y + (i * 2) + 3,
                    f"{graph.style(0)}{graph.foreColor(self.OPTIONNAMES[i]["color"])}{"".join([sucoV(self.OPTIONNAMES[i]["color"]) for x in range(26)])}{graph.Reset.STYLE}"
                )
            Print2D.coord(
                self.position.x + 4,
                self.position.y + (i * 2) + 3,
                f"{graph.ForeColors[self.OPTIONNAMES[i]["color"]]["color"]}[{self.OPTIONNAMES[i]["icon"]}] {(graph.ForeColors[self.OPTIONNAMES[i]["color"]]["color"]) if self.currentId == i else (graph.ForeColors[14]["color"])}{Print2D.getStr(self.position.x + 8 + (sucoIV(i) * 2), self.position.y + (i * 2) + 3,)}{sucoIII(i, True)}{sucoII(i)}{sucoIII(i, False)}{graph.Reset.STYLE}"
            )

    def open(self):
        self.canRender = True
        while self.canRender:
            
            self.render()
            self.currentRState = self.RenderState.OPTIONS

            if msvcrt.kbhit():
                self.readKey(kInput.getKeyPressed())
                self.currentRState = self.RenderState.ALL

            time.sleep(0.05)
            
        Print2D.clear()

    def render(self):

        
        self.renderOptions()

        if self.currentRState != self.RenderState.ALL:
            return 

        self.msp.renderTitle(Vector2(2,25), self.OPTIONNAMES[self.currentId]["color"])
        self.mainPanel.subTitle = self.OPTIONNAMES[self.currentId]["icon"]
        self.msp.clock.render()
        self.mainPanel.colorId = self.OPTIONNAMES[self.currentId]["color"]
        self.mainPanel.render(True)
        self.renderSug()

    def key(self):
        pass

    def changeId(self, add: bool):
        if add:
            self.currentId = min(max(0,self.currentId + 1),len(self.OPTIONNAMES) - 1)
        else:
            self.currentId = min(max(0,self.currentId - 1),len(self.OPTIONNAMES) - 1)

    def readKey(self, key: str):
        match key:
            case "accept":
                self.action()

            case "up":
                self.changeId(False)

            case "down":
                self.changeId(True)

            case _:
                pass

    def action(self):
        match self.currentId:
            case 0:
                self.canRender = False

            case 1:
                self.canRender = False
                self.msp.stop()

            case 2:
                self.canRender = False
                self.msp.newDraw(True)

            case 3:
                self.canRender = False
                self.msp.renderInterface()
                self.msp.openLoad()

            case 4:
                self.canRender = False
                self.msp.renderInterface()
                self.msp.openSave()

            case _:
                pass

    def renderSug(self):
        g = lambda string : kInput.getKey(string).upper()
        Print2D.coord(
            self.position.x + 2,
            self.mainPanel.margin.y + self.mainPanel.size.y,
            f"[{graph.foreColor(14)}{g('up')}{graph.Reset.STYLE}][{graph.foreColor(14)}{g('down')}{graph.Reset.STYLE}] SELECCIONAR" 
        )
        Print2D.coord(
            self.position.x + 2,
            self.mainPanel.margin.y + self.mainPanel.size.y + 1,
            f"[{graph.foreColor(4)}{g('accept')}{graph.Reset.STYLE}] SELECCIONAR" 
        )