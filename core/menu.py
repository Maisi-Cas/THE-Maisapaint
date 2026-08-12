# Clases utiles
from utils.vector2 import Vector2
from utils.print2d import Print2D

# Clases del motor
from engine.panel import Panel
import engine.graph as graph

# Clases del nucleo
import core.states as states
from core.inputHandler import kInput

class Menu:
    canRender = True
    isOpen = True
    OPTIONNAMES = [
        {"color" : 2, "name": "Volver", "icon" : ">"},
        {"color" : 0, "name": "Salir", "icon" : "<"},
        {"color" : 6, "name": "Cargar", "icon" : "^"},
        {"color" : 4, "name": "Guardar", "icon" : "v"}
    ]

    def __init__(self, position: Vector2, colorId: int, msp):
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
        for i in range(0, len(self.OPTIONNAMES)):
            Print2D.coord(
                self.position.x + 4,
                self.position.y + (i * 2) + 3,
                f"{graph.ForeColors[self.OPTIONNAMES[i]["color"]]["color"]}[{self.OPTIONNAMES[i]["icon"]}] {(graph.ForeColors[self.OPTIONNAMES[i]["color"]]["color"]) if self.currentId == i else (graph.ForeColors[14]["color"])}    {suco(True, i)} {self.OPTIONNAMES[i]["name"]} {suco(False, i)}{graph.Reset.STYLE}"
            )

    def open(self):
        self.canRender = True
        while self.canRender:
            self.render()
            self.readKey(kInput.getKeyPressed())
        Print2D.clear()

    def render(self):
        self.mainPanel.render(True)
        self.renderOptions()

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

            case 3:
                self.canRender = False
                self.msp.renderInterface()
                self.msp.openSave()

            case _:
                pass
