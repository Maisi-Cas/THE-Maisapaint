# Clases utiles
from utils.vector2 import Vector2
from utils.print2d import Print2D
from core.inputHandler import kInput

# Clases del motor
from core.emitBus import bus
import engine.graph as graph
from engine.panel import Panel
from engine.tile import Tile
from engine.msgBox import MsgBox

# Clases de la UI
from ui.selector import Selector
from ui.selector import ColorSelector
from ui.selector import CharacterSelector
from ui.selector import StyleSelector

# Clases de Python
from typing import Literal
import os
import json
import re
from enum import Enum
from pathlib import Path
import random as rand
import core.polla as polla

class Load:

    class DrawSlot:

        class DrawSlotStates(Enum):
            EMPTY = 0
            READY = 1
            UNREADABLE = 2

        def __init__(self, position: Vector2, fileName:str):

            self.currentState = self.DrawSlotStates.EMPTY
            self.colorId = 12
            self.focus = False
            self.msgBox = MsgBox(position.copy(), 0)
            self.position = position.copy()
            self.tilePanel = Panel("", 12, self.position.sum(1,1), Vector2(1,1))
            self.dataPanel = Panel("", 12, self.position.sum(5,1), Vector2(22,1))
            self.date = ""
            self.draw = {}
            self.title = ""
            self.tile = Tile("!",0,15,0)
            self.setFile(fileName)
            self.backText = ""
            self.setBackGround()


        def render(self):

            match self.currentState:
                case self.DrawSlotStates.EMPTY:
                    self.setColor(3)

                case self.DrawSlotStates.UNREADABLE:
                    self.setColor(0)

                case self.DrawSlotStates.READY:
                    self.setColor(12)

            if self.focus:
                self.dataPanel.type = "double"
                self.tilePanel.type = "double"

                if self.currentState == self.DrawSlotStates.READY:
                    self.setColor(2)

            else:
                self.dataPanel.type = "normal"
                self.tilePanel.type = "normal"

            self.tilePanel.render()
            self.dataPanel.render(True)

            Print2D.coord(self.position.x + 5, self.position.y + 3, ":")
            Print2D.coord(self.position.x + 3, self.position.y + 3, self.tile.getString())

            print(graph.foreColor(self.colorId))
            print(graph.style(0))

            Print2D.coord(self.position.x + 7, self.position.y + 3, self.backText)
            

            print(graph.Reset.STYLE)
            print(graph.foreColor(self.colorId))

            Print2D.coord(self.position.x + 13, self.position.y + 4, self.date)
            Print2D.coord(self.position.x + 7, self.position.y + 3, self.title)

            print(graph.Reset.STYLE)

        def setColor(self, newId):
            self.colorId = newId
            self.tilePanel.colorId = newId
            self.dataPanel.colorId = newId

        def setBackGround(self):

            if self.currentState != self.DrawSlotStates.READY:
                return
            #inicio de la aportacion de IsraelGPT
            draw_data = str(self.draw.get("draw", "")).replace(" ", "")

            if len(draw_data) <= 22:
                self.backText = draw_data.ljust(22)
            else:
                start = rand.randint(0, len(draw_data) - 22)
                self.backText = draw_data[start:start + 22]
            #fin de la aportacion de israel gpt

        def renderIn(self, position: Vector2):
            self.changePosition(position.copy())
            self.render()

        def changePosition(self, position: Vector2):
            self.position = position.copy()
            self.tilePanel.margin = position.sum(1,1)
            self.dataPanel.margin = position.sum(5,1)

        def setFile(self, file: str):
            
            self.draw.clear()
            directory = f"draws/{file}.msp" 
            if os.path.exists(directory) and os.path.isfile(directory):

                try:
                    with open(directory, "r", encoding="utf-8") as f:
                        draw = json.load(f)

                    self.draw["date"] = draw["date"]
                    tile = draw["icon"]
                    self.tile.reset(tile[0], tile[1], tile[2], tile[3])
                    self.draw["draw"] = []
                    self.date = draw["date"]

                    for i in draw["layers"]:
                        alex = {}
                        alex["name"] = i["name"]
                        alex["enable"] = i["enable"]
                        alex["draw"] = {}

                        for j, (a, b, c ,d) in i["draw"].items():
                            s = j.split(",")
                            alex["draw"][(int(s[0]), int(s[1]))] = [a, b, c, d]

                        self.draw["draw"].append(alex.copy())

                    self.title = file.replace("-", " ")

                    holaSoyTransSans = False
                    for i in polla.tumamabank:
                        if i in self.title.lower():
                            holaSoyTransSans = True

                    if not holaSoyTransSans:
                        self.dataPanel.subTitleIndent = 19 - (len(str(self.countTiles())))
                        self.dataPanel.subTitle = graph.foreColor(self.countTiles() % 15) + str(self.countTiles()) + graph.Reset.STYLE
                        
                    else:
                        self.dataPanel.subTitleIndent = 19 - (len(str(99999999999)))
                        self.dataPanel.subTitle = graph.foreColor(11) + "99999999999" + graph.Reset.STYLE
                    self.currentState = self.DrawSlotStates.READY

                except Exception as e:
                    self.currentState = self.DrawSlotStates.UNREADABLE
                    self.title = str(e)[:22]

            else:
                self.currentState = self.DrawSlotStates.EMPTY

        def countTiles(self):
            circunsizo = 0

            for i in self.draw["draw"]:
                circunsizo += len(i["draw"])

            return circunsizo

    isRunning: bool

    def __init__(self, colorId, position: Vector2, ):
        self.SLOTS_PER_PAGE = 4
        self.currentPage = 0
        self.msgBox = MsgBox(position.copy(), 0)
        self.title = ". . ."
        self.currentSlot = 0
        self.position = position.copy()
        self.mainPanel = Panel("Cargar", colorId, position.copy(), Vector2(44, 15))
        self.tilePanel = Panel("", 12, self.position.sum(10,6),Vector2(1,1))
        self.titlePanel = Panel("Nombre", 12, self.position.sum(14,6), Vector2(21,1))
        self.slots = []
        self.slotsPanel = Panel("Dibujos", 14, self.position.sum(8,2), Vector2(28, 12))
        self.slotsPanel.subTitleIndent = 10
        

    def setSlots(self):
        self.slots.clear()

        if os.path.exists("draws") and os.path.isdir("draws"):
            for archivo in Path("draws").glob("*.msp"):
                self.slots.append(self.DrawSlot(Vector2(1,1), archivo.stem))
            self.isRunning = True
        else:
            self.msgBox.get("Sin carpeta", "No se encontró la carpeta draws, guarde un dibujo para crearla")
            self.isRunning = False


    def open(self):
        self.setSlots()
        self.inicio = self.currentPage * self.SLOTS_PER_PAGE
        self.fin = min(self.inicio + self.SLOTS_PER_PAGE, len(self.slots))
        self.update()
        
        while self.isRunning:
            self.render()

            match kInput.getKeyPressed():
                case 'up':
                    self.select(True)

                case 'down':
                    self.select(False)
                case 'left':
                    self.selectPage(True)
                case 'right':
                    self.selectPage(False)
                case 'cancel':
                    self.isRunning = False
                case 'accept':
                    self.load()
                    self.isRunning = False
                case _:
                    pass

        Print2D.clear()


    def render(self):
        self.mainPanel.render(True)
        self.renderSlots()
        self.slotsPanel.render()



    def renderSlots(self):
        self.inicio = self.currentPage * self.SLOTS_PER_PAGE

        self.fin = min(self.inicio + self.SLOTS_PER_PAGE, len(self.slots))

        for i in range(self.inicio, self.fin):
            self.slots[i].renderIn(self.position.sum(8, 2+(i-self.inicio) * 3))

    def update(self):
        for i in self.slots:
            i.focus = False

        self.currentSlot = min(max(0, self.currentSlot), len(self.slots) - 1)
        if self.slots:
            self.slots[self.currentSlot].focus = True

        self.slotsPanel.subTitle = f"{str(self.currentPage + 1)}/{self.getPageCount()}"

    def select(self, boo):
        if not boo:
            self.currentSlot += 1
        else:
            self.currentSlot -= 1

        self.currentSlot = min(max(self.inicio, self.currentSlot), self.fin - 1)
        self.update()

    def selectPage(self, boo):
        if not boo:
            self.currentPage += 1
            self.currentSlot += self.SLOTS_PER_PAGE
        else:
            self.currentPage -= 1
            self.currentSlot -= self.SLOTS_PER_PAGE

        if len(self.slots) % self.SLOTS_PER_PAGE:
            self.currentPage = min(max(0, self.currentPage), len(self.slots) // self.SLOTS_PER_PAGE)
        else:
            self.currentPage = min(max(0, self.currentPage), (len(self.slots) // self.SLOTS_PER_PAGE) + 1) 

        self.inicio = self.currentPage * self.SLOTS_PER_PAGE
        
        self.fin = min(self.inicio + self.SLOTS_PER_PAGE, len(self.slots))   

        self.currentSlot = min(max(self.inicio, self.currentSlot), self.fin - 1)
        self.update()

    def getPageCount(self):
        return (len(self.slots) + self.SLOTS_PER_PAGE - 1) // self.SLOTS_PER_PAGE

    def load(self):
        if self.slots[self.currentSlot].currentState == self.DrawSlot.DrawSlotStates.READY:
            bus.emit("load-draw", self.slots[self.currentSlot].draw["draw"].copy())
            bus.emit("change-name", self.slots[self.currentSlot].title, self.slots[self.currentSlot].tile.copy())

