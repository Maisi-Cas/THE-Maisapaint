# Clases utiles
from utils.vector2 import Vector2
from utils.print2d import Print2D
from core.inputHandler import kInput

# Clases del nucleo
import core.polla as polla
from core.emitBus import bus

# Clases del motor
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
from datetime import datetime

class Save:
    isRunning: bool

    def __init__(self, colorId, position: Vector2):

        self.msgBox = MsgBox(position.copy(), 0)
        self.title = ". . ."
        self.currentSelector = 0
        self.position = position.copy()
        self.mainPanel = Panel("Guardar", colorId, position.copy(), Vector2(45, 15))
        self.selectors : Selector = [
            ColorSelector(self.position.sum(1,12), "Color"),
            CharacterSelector(self.position.sum(19,12), "Caracter"),
            ColorSelector(self.position.sum(5,15), "Fondo"),
            StyleSelector(self.position.sum(23,15), "Estilo")
        ]
        self.tilePanel = Panel("", 12, self.position.sum(10,6),Vector2(1,1))
        self.titlePanel = Panel("Nombre", 12, self.position.sum(14,6), Vector2(21,1))
        
        for i in self.selectors: #Deja a todos los selctores de color blanco
            i.colorId = 12
        self.selectors[self.currentSelector].colorId = 2
        self.tile = Tile(graph.Characters[self.selectors[1].currentId]["character"], self.selectors[0].currentId, self.selectors[2].currentId, self.selectors[3].currentId)
        
        self.addsubtitile()

        bus.conect('send-draw-name', self.setDrawName)


    def open(self, draw: dict):
        self.getDrawName()

        self.isRunning = True
        self.render()
        
        while self.isRunning:
            self.render()

            match kInput.getKeyPressed():
                case "accept":
                    self.sendSRTP()
                    self.save(draw.copy())
                    self.isRunning = False
                case "up":
                    self.nav('u')

                case "down":
                    self.nav('d')

                case "left":
                    self.nav('l')

                case "right":
                    self.nav('r')

                case "extra-0":
                    self.writeName()

                case "cancel":
                    self.isRunning = False

                case _:
                    pass
                

    def render(self):
        self.mainPanel.render(True)
        self.renderIndications()
        Print2D.coord(self.position.x + 2, self.position.y + 6, graph.foreColor(14) + "NO PUEDEN HABER 2 DIBUJOS CON EL MISMO NOMBRE" + graph.Reset.STYLE)
        Print2D.coord(self.position.x + 2, self.position.y + 10, graph.foreColor(14) + "SELECCIONE UN TILE PARA REPRESENTAR SU DIBUJO" + graph.Reset.STYLE)
        self.tilePanel.render()
        self.titlePanel.render()
        self.renderSelectors()
        Print2D.coord(self.position.x + 14, self.position.y + 8, ":")
        Print2D.coord(self.position.x + 12, self.position.y + 8, self.tile.getString())

        if self.blackNameList():
            Print2D.coord(self.position.x + 16, self.position.y + 8, graph.foreColor(14) + self.title + graph.Reset.STYLE)
        else:
            Print2D.coord(self.position.x + 16, self.position.y + 8, graph.foreColor(12) + self.title + graph.Reset.STYLE)

    def renderSelectors(self):
        for i in self.selectors:
            i.render()

    def nav(self, direction: Literal['u','d','l','r'] = 'r'):
        for i in self.selectors: #Deja a todos los selctores de color blanco
            i.colorId = 12
        
        match direction:
            # En el caso de [u] y [d], alternas de selector 
            case 'u':
                if self.currentSelector != 0:
                    self.currentSelector -= 1
                else:
                    self.currentSelector = len(self.selectors) - 1
            case 'd':
                if self.currentSelector != len(self.selectors) - 1:
                    self.currentSelector += 1
                else:
                    self.currentSelector = 0
            # Y con [r] y [l], cambias el valor del selectoor
            case 'r':
                self.selectors[self.currentSelector].moveSelector('r')
                
            case 'l':
                self.selectors[self.currentSelector].moveSelector('l')

        self.tile = Tile(graph.Characters[self.selectors[1].currentId]["character"], self.selectors[0].currentId, self.selectors[2].currentId, self.selectors[3].currentId)
        self.addsubtitile()
        self.selectors[self.currentSelector].colorId = 2 # Deja el selector selccionado (XD) de color dorado

    def addsubtitile(self):
        match self.currentSelector:
            case 0:
                self.selectors[3].panel.subTitle = graph.ForeColors[3]['color'] + kInput.getKey('up').upper()
                self.selectors[1].panel.subTitle = graph.ForeColors[3]['color'] + kInput.getKey('down').upper()
                self.selectors[0].panel.subTitle = ''
                self.selectors[2].panel.subTitle = ''
            case 1:
                self.selectors[0].panel.subTitle = graph.ForeColors[3]['color'] + kInput.getKey('up').upper()
                self.selectors[2].panel.subTitle = graph.ForeColors[3]['color'] + kInput.getKey('down').upper()
                self.selectors[1].panel.subTitle = ''
                self.selectors[3].panel.subTitle = ''
            case 2:
                self.selectors[1].panel.subTitle = graph.ForeColors[3]['color'] + kInput.getKey('up').upper()
                self.selectors[3].panel.subTitle = graph.ForeColors[3]['color'] + kInput.getKey('down').upper()
                self.selectors[2].panel.subTitle = ''
                self.selectors[0].panel.subTitle = ''
            case 3:
                self.selectors[2].panel.subTitle = graph.ForeColors[3]['color'] + kInput.getKey('up').upper()
                self.selectors[0].panel.subTitle = graph.ForeColors[3]['color'] + kInput.getKey('down').upper()
                self.selectors[3].panel.subTitle = ''
                self.selectors[1].panel.subTitle = ''

    def writeName(self):
        self.titlePanel.render(True)
        print(graph.foreColor(2))
        Print2D.cursePos(self.titlePanel.margin.x + 2, self.titlePanel.margin.y + 2)
        title = input()
        if title:
            self.title = title[:21]

        print(graph.Reset.STYLE)

    def renderIndications(self):
        g = lambda string : kInput.getKey(string).upper()
        Print2D.coord(self.position.x + 2, self.position.y + 4, f"[{graph.foreColor(14)}{g("up")}{graph.Reset.STYLE}][{graph.foreColor(14)}{g("down")}{graph.Reset.STYLE}] CAMBIAR DE SELECTOR")
        Print2D.coord(self.position.x + 2, self.position.y + 5, f"[{graph.foreColor(14)}{g("left")}{graph.Reset.STYLE}][{graph.foreColor(14)}{g("right")}{graph.Reset.STYLE}] SELECCIONAR")
        Print2D.coord(self.position.x + 2, self.position.y + 2, f"[{graph.foreColor(0)}{g("cancel")}{graph.Reset.STYLE}] CANCELAR [{graph.foreColor(4)}{g("accept")}{graph.Reset.STYLE}] GUARDAR")
        Print2D.coord(self.position.x + 2, self.position.y + 3, f"[{graph.foreColor(2)}{g("extra-0")}{graph.Reset.STYLE}] EDITAR NOMBRE")

    def save(self, draw):
        # Primero revisemos que exite la carpeta
        if re.search(r'[\\/:*?"<>|]', self.title) or self.blackNameList():
            self.msgBox.get("Titulo no valido", 'Desafortunadamente el nombre de tu dibujo posee caracteres no validos >>([\\/:*?"<>|])<< o está en la lista negra')
            bus.emit('maisapaint-render')
            self.open(draw.copy())
            return
        directory = f"draws/{self.title.replace(" ", "-")}.msp"
        if os.path.exists("draws") and os.path.isdir("draws"):
            if os.path.exists(directory) and os.path.isfile(directory):
                if self.msgBox.getYesNo("Sobreescribir", f'Se ha encontrado otro archivo con el nombre {f"{self.title.replace(" ", "-")}.json"}, desea sobreescribirlo?'):
                    self.write(draw.copy())
                else:
                    bus.emit('maisapaint-render')
                    self.isRunning = True
                    self.open(draw.copy())
                    return
                
            else:
                self.write(draw.copy())
        else:
            os.mkdir("draws")
            self.writeReadme()
            self.write(draw.copy())
            

    def write(self, draw):
        directory = f"draws/{self.title.replace(" ", "-")}.msp"
        sonichu = {}
        sonichu["iconsp"] = [x.currentId for x in self.selectors]
        sonichu["format"] = {"format" : "msp", "version" : 1}
        sonichu["date"] = datetime.now().strftime("%d-%m-%Y %H:%M")
        sonichu["icon"] = [self.tile.character, self.tile.foreColorId, self.tile.backColorId, self.tile.styleId]
        sonichu["layers"] = []

        for i in draw:
            hatsuneMiku = {}
            hatsuneMiku["name"] = i["name"]
            hatsuneMiku["enable"] = i["enable"]
            hatsuneMiku["draw"] = {}
            for (x,y), (a,b,c,d) in i["draw"].items():
                hatsuneMiku["draw"][f"{x},{y}"] = [a, b, c, d]
            sonichu["layers"].append(hatsuneMiku)

        with open(directory, 'w', encoding='utf-8', ) as f:
            json.dump(sonichu, f, ensure_ascii=False)

        bus.emit('change-name', self.title, self.tile.copy())

    def writeReadme(self):
        directory = f"draws/readme.txt"
        pd = f"Si logras leer esto, tienes mi humor \n{self.title * 10}" if "polla" in self.title.lower() else f"Bravo tu primer dibujo se llama {self.title}"

        if polla.chekUrMonInStr(self.title):
            pd = "Estoy decepcionado de ti, seguramente\nalguien te dijo sobre el easter Egg"

        msg = [
            "Genial estás leyendo esto",
            "Me imagino que es por que probablemente",
            "hayas notado un nuevo archivo, aca se guardan",
            "los dibujos en un formato llamado msp, asi que una cosita,",
            "de preferencia",
            "NO TOQUES NADA, O TODO SE VA A LA-",
            "",
            "Con cariño el creador de MSP",
            "",
            pd
        ]

        with open(directory, "w", encoding="utf-8") as f:
            f.writelines(line + "\n" for line in msg)

    def blackNameList(self):
        blackList = [
            "Dibujo sin nombre",
            ". . ."
        ]

        for i in blackList:
            if i == self.title:
                return True

        return False

    def getDrawName(self):
        bus.emit("get-draw-name")

    def sendSRTP(self):
        bus.emit("change-s-r-t-p", [x.currentId for x in self.selectors])

    def setDrawName(self, name: str, selectorPosition: list):
        self.title = name

        for i in range(len(self.selectors)):
            selectorPosition[i] = min(max(0, selectorPosition[i]), len(self.selectors[i].ids) - 1)
            self.selectors[i].currentId = selectorPosition[i]

        self.tile.reset(graph.Characters[self.selectors[1].currentId]["character"], self.selectors[0].currentId, self.selectors[2].currentId, self.selectors[3].currentId)