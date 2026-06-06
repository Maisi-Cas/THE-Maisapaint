# MAISAPAINT.PY (Mejorado y con comentarios)

# Librerias de Python
import random as rand
from typing import Literal
import ctypes
import os
import json
import msvcrt
import time
import psutil

# Clases del motor
import engine.graph as graph
from engine.tile import Tile
from engine.curse import Curse
from engine.panel import Panel
from engine.layer import Layer, LayerMaster
from engine.table import Table
from engine.msgBox import MsgBox

# Clases del nucleo
from core.emitBus import bus
from core.inputHandler import kInput
import core.states as states

# Clases/Recursos utiles (Estos 2 papuchos son los que mantienen el programa en funcionamiento)
from utils.vector2 import Vector2 
from utils.print2d import Print2D as print2d

# Interfaz de usuario
from ui.canvas import Canvas
from ui.clock import Clock
from ui.tileSelector import TileSelector
from ui.textBox import TextBox
from ui.selector import ColorSelector, CharacterSelector, StyleSelector


# CLASE PRINCIPAL, LA CLASE DE CLASES, EL DIOS DE LA CLASE
class Maisapaint:
    # Tenia planeado hacer esta clase en otro archivo pero me dio paja y mejor la declare aca
    class SplashText:
        def __init__(self, position: Vector2, size: Vector2):
            
            print2d.clear()
            chargeString = ['The#MSPaint por Maisi','Hecho en Python','Cargando...']
            time.sleep(0.01)
            for i in chargeString:
                for j in range(len(i)):
                    randNum = rand.randint(0, len(graph.ForeColors) - 2)
                    print(graph.ForeColors[randNum]['color'] + i[j] + graph.Reset.STYLE, end='', flush=True)                
                    time.sleep(0.01)
                print()
            time.sleep(0.7)                                                    
            
                
            self.postion = position.copy()
            self.size = size.copy()
            
            self.splashText = ""
            
            with open('data/splashTexts.json', 'r') as splashTexts:
                self.splashText = rand.choice(json.load(splashTexts)['normal'])
            
            self.textBox = TextBox(self.postion.copy(), self.size.copy(), self.splashText, 2)
            self.panel = Panel('Texto chistoso', 6, self.postion - 2, self.size.copy())
            
        def render(self):
            self.panel.render()
            self.textBox.render()
    
    class KeyTable:
        def __init__(self, position: Vector2):
            self.table = Table("Controles", 5, position.copy(), 2, 20)
            self.table.setColSize([9,16])
            self.table.setColors([7],[3,11])
            self.table.setHeadings("Tecla", "Accion")
            self.valueDict = {
                'draw' : [
                    ["W A S D", "MOVERSE"],
                    ["J", "DIBUJAR"],
                    ["K", "BORRAR"],
                    ["Q E", "SELECCIONAR TILE"],
                    ["F", "MODO SELECCION"],
                    ["R", "MODO CAPA"],
                    ["Z", "LIMPIAR DIBUJO"],
                    ["X", "ALTERNAR DIBUJO RAPIDO"],
                    ["I", "OCULTAR CURSOR"],
                    ["V", "CUBETA"],
                    ["Y", "SALIR"]
                    
                ],
                'select' : [
                    ["W S", "CAMBIAR SELECTOR"],
                    ["A D", "CAMBIAR VALOR"],
                    ["J", "AÑADIR TILE"],
                    ["Q E", "SELECCIONAR TILE"],
                    ["R", "MODO CAPA"],
                    ["F", "MODO DIBUJO"],
                    ["C", "CUSTOMIZAR CARACTER"],
                    ["Y", "SALIR"]
                ],
                'layer' : [
                    ["W S", "SELECCIONAR CAPA"],
                    ["A D", "OCULTAR Y MOSTRAR CAPA"],
                    ["R J", "MODO DIBUJO"],
                    ["F", "MODO CAPA"],
                    ["C", "RENOMBRAR CAPA"],
                    ["Y", "SALIR"]
                ]
            }
            self.update()
            
        def update(self):
            self.table.clear()
            key = ''
            match states.current:
                case states.States.DRAW:
                    key = 'draw'
                case states.States.SELECTCOLOR:
                    key = 'select'
                case states.States.LAYER:
                    key = 'layer'
                    
            
            for i in self.valueDict[key]:
                self.table.addContet(i[0], i[1])
                
        def render(self):
            self.table.show()
    
    class FillClass:
        def __init__(self, position: Vector2, x, colorId):
            self.text = "tniapasiaM#EHT"
            self.x = x
            self.colorList = []
            self.position = position.copy()
            self.panel = Panel("", 14, position - 1, Vector2(x, 1))
            self.index = 0
            bus.conect('draw-clear', self.clear)
            
        def render(self):
            self.panel.render()
            counter = 0
            for i in self.colorList:
                print2d.coord(self.position.x + counter + 1, self.position.y + 1, graph.BackColors[i[0]]["color"] + graph.ForeColors[15]["color"] + i[1] + graph.Reset.STYLE)
                counter += 1
                
        def add(self, id):
            self.colorList.insert(0, [id, self.text[self.index]])
            if len(self.colorList) > self.x:
                self.colorList.pop()
                
            self.index += 1
            if self.index == len(self.text):
                self.index = 0
                
        def clear(self):
            self.panel.render(True)
            self.colorList = []
            self.index = 0
    
    class Info:
        def __init__(self, position: Vector2, ancho: int, colorId: int, father):
            self.father = father
            self.position = position.copy()
            self.size = Vector2(ancho, 9)
            self.colorId = colorId
            self.panel = Panel('Info', self.colorId, self.position.copy(), self.size.copy())
        
        def render(self):
            process = psutil.Process(os.getpid())
            memoria = process.memory_info().rss

            self.panel.render(True)
            strings = [
                f'CURSOR : ({graph.ForeColors[2]['color']}{self.father.curse.position.x}{graph.Reset.STYLE}, {graph.ForeColors[5]['color']}{self.father.curse.position.y}{graph.Reset.STYLE})',
                f'TILE : [{self.father.tileSelector.tiles[self.father.tileSelector.currenTile].getString()}]',
                f'T. DIBUJADOS : {graph.ForeColors[self.father.layermaster.countTiles() % 15]['color']}{self.father.layermaster.countTiles()}{graph.Reset.STYLE}',
                f'CAPA : {graph.ForeColors[3]['color']}{self.father.layermaster.layers[self.father.layermaster.currentId]["name"]}{graph.Reset.STYLE}',
                f'MODO : {graph.ForeColors[7]['color']}{states.current.name}{graph.Reset.STYLE}',
                f'V : {graph.ForeColors[9]['color']}{self.father.version}{graph.Reset.STYLE}',
                f'MEMORIA : {graph.ForeColors[5]['color']}{round(memoria/(1024 ** 2),4)} MB{graph.Reset.STYLE}'
                
            ]
            for i in range(len(strings)):
                print2d.coord(self.position.x + 2, self.position.y + 2 + i, strings[i])
    
    def __init__(self):
        self.version = '(Alpha) #1'
        self.canRun = True
        self.fastDrawMode = False
        # Declaracion de los Paneles/Frames
        self.superPanel = Panel(f"{graph.ForeColors[0]['color']}T{graph.ForeColors[5]['color']}H{graph.ForeColors[8]['color']}E{graph.ForeColors[2]['color']}#{graph.ForeColors[1]['color']}M{graph.ForeColors[2]['color']}a{graph.ForeColors[3]['color']}i{graph.ForeColors[4]['color']}s{graph.ForeColors[6]['color']}a{graph.ForeColors[7]['color']}p{graph.ForeColors[9]['color']}a{graph.ForeColors[10]['color']}i{graph.ForeColors[11]['color']}n{graph.ForeColors[12]['color']}t", rand.randint(0, 14), Vector2(0,0), Vector2(100,29))
        self.mainpanel = Panel('Dibujo', 12, Vector2(28,4), Vector2(48,16))
        self.tileSelector = TileSelector(Vector2(30,3), 16)
        self.splashtext = self.SplashText(Vector2(3,3), Vector2(25,5))
        self.selectorPanel = Panel(
            'Selectores',
            7,
            Vector2(
                self.mainpanel.margin.x,
                self.mainpanel.margin.y + self.mainpanel.size.y + 2
            ),
            Vector2(
                self.mainpanel.size.x,
                6    
            )
        )
        self.keytable = self.KeyTable(Vector2(self.splashtext.postion.x - 1, self.splashtext.postion.y + self.splashtext.size.y + 1))
        # Lista que almacena los selectores tomando como referencia las cordenadas del objeto SelectorPanel
        self.selectors = [
            ColorSelector(Vector2(
                self.selectorPanel.margin.x + 2,
                self.selectorPanel.margin.y + 3
                ),
            'Fuente'
            ),
            CharacterSelector(
                Vector2(
                    self.selectorPanel.margin.x + 21,
                    self.selectorPanel.margin.y + 3
                ),
            'Caracter'
            ),
            ColorSelector(Vector2(
                self.selectorPanel.margin.x + 2,
                self.selectorPanel.margin.y + 6
                ),
            'Fondo' 
            ),
            StyleSelector(Vector2(
                self.selectorPanel.margin.x + 29,
                self.selectorPanel.margin.y + 6
                ),
            'Estilo' 
            )
        ]
        self.selectors[2].currentId = 15
        self.currentSelector = 0
        # Otras cosas
        
        self.clock = Clock(Vector2(self.selectorPanel.margin.x + 23, self.selectorPanel.margin.y + 6)) # Reloj
        self.selectorPanelTile = Tile(graph.Characters[self.selectors[1].currentId]["character"], self.selectors[0].currentId, self.selectors[2].currentId, 1)
        self.selectorPanel.title = f"[{self.selectorPanelTile}{graph.ForeColors[self.selectorPanel.colorId]['color']}]Selectores"
        """
            A ver, abro esto para explicar algo sobre [self.SelectorPanelTile:Tile] y de [self.SelectorPanel.title:str]
            Debí haber hecho una clase, pero soy tremendo vago y mejor aca declaré estas variables, ni que me fuera a morir
            [self.SelectorPanelTile] : Es un objeto de tipo tile, este es el tile que se forma según los valores de los selectores
            [self.SelectorPanel.title] : Pone el tile en el titulo, algo asi [$]Selectores
        """
        
        # Curse y Layer, sin estos 2 papasotes, no hay dibujo
        self.curse = Curse(
            self.mainpanel.margin.copy(),
            self.mainpanel.size.copy(),
            Vector2(self.mainpanel.size.x // 2, self.mainpanel.size.y // 2)
        )
        self.curse.colorId = self.tileSelector.tiles[self.tileSelector.currenTile].foreColorId
        self.draw = Layer(Vector2(self.mainpanel.margin.x + 1, self.mainpanel.margin.y + 1), self.mainpanel.size.copy())
        self.oh = self.FillClass(
            Vector2(
                self.splashtext.size.x + self.mainpanel.size.x + 6,
                2
            ),
            21,
            14
        )
        self.layermaster = LayerMaster(
            2,
            Vector2(
                self.splashtext.size.x + self.mainpanel.size.x + 6,
                5
            ),
            Vector2(21,13)
        )
        self.layermaster.connect(self.draw)
        self.msgBox = MsgBox(self.mainpanel.margin + 2, 0)
        self.cMsgBox = MsgBox(Vector2(self.mainpanel.margin.x, self.mainpanel.margin.y + 5), 0)
        self.lrmsgBox = MsgBox(Vector2(self.layermaster.margin.x - 20, self.layermaster.margin.y),7)
        self.info = self.Info(
            Vector2(self.selectorPanel.margin.x + self.selectorPanel.size.x + 2, self.layermaster.size.y + self.layermaster.margin.y + 1),
            self.layermaster.size.x,
            10,
            self
        )
        
        # Conectar señales
        bus.conect('draw-tile', self.drawTile)
        bus.conect('mp-stop', self.stop)
        bus.conect('slct-move', self.select)
        bus.conect('state-change', self.changeState)
        bus.conect('erase-tile', self.eraseTile)
        bus.conect('cstm-char', self.custimizeChar)
        bus.conect('slct-tile-change', self.changeTile)
        bus.conect('show-cmd-cursor', self.showCMDCurse)
        bus.conect('slct-tile', self.updateCurse)
        bus.conect('move-curse', self.fastDraw)
        bus.conect('fast-mode', self.fastDrawModeToogle)
        bus.conect('rnme-layer', self.renameLayer)
        bus.conect('draw-clear', self.clear)
        bus.conect('fill-layer', self.fill)

    # region Run  
    # Funcion que corre el programa    
    def run(self):
        self.showCMDCurse(False) # Esto en teoria elimina el cursor del cmd, me sorprende que funcione, debo hacer la version Show
        print2d.clear() # Escribe cls en CMD, es eso basicamente
        
        self.superPanel.render()
        self.renderTitle(Vector2(2,2))
        msvcrt.getch()
        self.superPanel.render(True)
        
        while(self.canRun):
            
            states.isRendering = True #Esta cochinada la hice por que el reloj me jodia el ui
            
            if not states.clockIsRendering:
                #Renderizar
                self.renderInterface()
                self.info.render()
                
                states.isRendering = False
                states.currentFlag = states.Flags.NONE
                kInput.inputHandler()
        
        self.superPanel.title = "BYE BYE ;)"
        self.superPanel.render(True)
        self.renderTitle(Vector2(2,2))
        self.superPanel.render()
        self.showCMDCurse(True)
        
    # endregion
    
    # region Renders
    def renderInterface(self):
        match states.current:
            case states.States.DRAW:
                self.renderDraw()
            case states.States.SELECTCOLOR:
                self.renderSelection()
            case states.States.LAYER:
                self.renderLayer()
    
    def renderDraw(self):
        match states.currentFlag:
            case states.Flags.NONE:
                self.superPanel.render()
                self.selectorPanel.render()
                self.keytable.render()
                for i in self.selectors:
                    i.render()
                # Cuando le pones true al render de un panel, este hace un limpiado de pantalla local
                self.splashtext.render()
                self.tileSelector.render()
                self.layermaster.render() 
                self.mainpanel.render(True)
                self.layermaster.renderDraws()
                self.oh.render()
                self.curse.render()
                self.clock.render()
                
            case states.Flags.DRAW:
                self.oh.render()
                self.mainpanel.render(True)
                self.layermaster.render() 
                self.layermaster.renderDraws()
                self.curse.render()
                self.clock.render()
            
            case states.Flags.MOVE:
                self.mainpanel.render(True)
                self.layermaster.renderDraws() 
                self.curse.render()
                self.clock.render()
            
            case states.Flags.CTILE:
                self.tileSelector.render()
                self.curse.render()
                self.clock.render()
            
            case states.Flags.ULAYER:
                self.mainpanel.render(True)
                self.layermaster.render()
                self.layermaster.renderDraws()
                self.curse.render()
                self.clock.render()
            
            case states.Flags.PASS:
                pass

    def renderSelection(self):
        match states.currentFlag:
            case states.Flags.NONE:
                self.superPanel.render()
                self.selectorPanel.render()
                self.mainpanel.render()
                self.splashtext.render()
                self.keytable.render()
                self.tileSelector.render()
                for i in self.selectors:
                    i.render()
                self.layermaster.render()
                self.layermaster.renderDraws()
                self.oh.render()
                self.curse.render()
                self.clock.render()
            
            case states.Flags.SELECTION:
                self.selectorPanel.render()
                for i in self.selectors:
                    i.render()
                self.clock.render()
            
            case states.Flags.CTILE:
                self.tileSelector.render()
                self.curse.render()
                self.clock.render()
            
            case states.Flags.PASS:
                pass
    
    def renderLayer(self):
        match states.currentFlag:
            case states.Flags.NONE:
                self.superPanel.render()
                self.selectorPanel.render()
                self.mainpanel.render(True)
                self.splashtext.render()
                self.keytable.render()
                self.tileSelector.render()
                for i in self.selectors:
                    i.render()
                self.layermaster.render()
                self.layermaster.renderDraws()
                self.oh.render()
                self.clock.render() 

            case states.Flags.CLAYER:
                self.layermaster.render()
                self.clock.render()
                
            case states.Flags.ULAYER:
                self.mainpanel.render(True)
                self.layermaster.render()
                self.layermaster.renderDraws()
                self.clock.render()
                
    def renderTitle(self, position: Vector2):
        "0 5 8 2 1 4 7 9 10 11 12"
        
        title = [
            f'┌───────────┬─┬─┐┌─────┬─────────────────────┐  ┌────┐',
            f'└─┐ ┌─┬─┬───┘   └┤     │ ──┬───┬───┬─┬───┐ ┌─┘┌─┴─── ├─┐', 
            f'  │ │   │ ──  + ─┤ │ │ ├─┐ │ + │ - │ │   │ │  │ ┌────┘ │',
            f'  │ │ │ │ ──┐   ┌┴─┴─┴─┴─┘ │ ┌─┤ │ │ │ │ │ │  └─┤ ───┬─┘',
            f'  └─┴─┴─┴───┴─┴─┴──────────┤ │ └─┴─┴─┴─┴─┴─┘    └────┘',
            f'                           └─┘'
        ]
        print(graph.ForeColors[self.superPanel.colorId]['color'])
        for i in range(len(title)):
            print2d.coord(position.x, position.y + i, title[i])
        print(graph.Reset.STYLE)
                    
    # endregion
    # Esta cosa es lo que permite navegar por los selectores
    def select(self, direction: Literal['u','d','l','r'] = 'r'):
        states.currentFlag = states.Flags.SELECTION
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
            
        self.selectors[self.currentSelector].colorId = 2 # Deja el selector selccionado (XD) de color dorado
        
        # Y ya se aplican los cambios al selector de tiles
        self.selectorPanelTile = Tile(graph.Characters[self.selectors[1].currentId]["character"], self.selectors[0].currentId, self.selectors[2].currentId, self.selectors[3].currentId)
        self.selectorPanel.title = f"[{self.selectorPanelTile}{graph.ForeColors[self.selectorPanel.colorId]['color']}]Selectores"
    
    # Agrega un tile a la clase layermaster, tomando el tile del tileSelector y las posision del cusror                
    def drawTile(self):
        states.currentFlag = states.Flags.DRAW
        self.layermaster.addpixel(self.curse.position.copy(), self.tileSelector.tiles[self.tileSelector.currenTile].copy())
        self.oh.add(self.tileSelector.tiles[self.tileSelector.currenTile].foreColorId)
    
    # Borra owo    
    def eraseTile(self):
        self.layermaster.deletePixel(self.curse.position.x, self.curse.position.y)
    
    # En serio debo explicar que hace esta linea?    
    def stop(self):
        
        self.canRun = not self.msgBox.getYesNo('Confirmar', 'Esta seguro de querer salir de THE#MSPaint?')

    # Cuando se cambia el estado, configura unas cositas
    def changeState(self, state: states.States.DRAW):
        states.currentFlag = states.Flags.NONE
        print2d.clear()
        states.current = state
        
        match states.current:
            case states.States.DRAW:
                for i in self.selectors:
                    i.colorId = 12 # Decolorar selectores
                    
            case states.States.SELECTCOLOR:
                self.selectors[self.currentSelector].colorId = 2 # Colorear de dorado el selecor actual
        
        self.keytable.update()
    
    # CTRL + C, CTRL + V De israel gpt, ni idea que hacer pero me gusta
    # Oculta o muestra el cursor del cms                
    def showCMDCurse(self, value: bool):
        class CursorInfo(ctypes.Structure):
            _fields_ = [
                ("size", ctypes.c_int),
                ("visible", ctypes.c_byte),
            ]

        handle = ctypes.windll.kernel32.GetStdHandle(-11)

        cursor = CursorInfo()
        ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(cursor))

        cursor.visible = value

        ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(cursor))
        
    def setCMDSize(self, x, y): # En progreso
        pass
    
    # Esta cosa se activa cuando customizas el caracter                    
    def custimizeChar(self):
        self.cMsgBox.position = Vector2(self.mainpanel.margin.x + self.selectors[1].currentId, self.mainpanel.margin.y + 5)
        if graph.Characters[self.selectors[1].currentId]['customizable']:
            self.cMsgBox.colorId = 11
            sanseeeee = self.cMsgBox.getText("Customizar", f"Ingresa el caracter con el que vas a reemplazar [{graph.Characters[self.selectors[1].currentId]['character']}]", 1)
            if sanseeeee['state']:
                graph.Characters[self.selectors[1].currentId]['character'] = sanseeeee['string']
        else:
            self.cMsgBox.colorId = 0
            self.cMsgBox.get("UPS...", "Este caracter no es customizable, los caracteres customizables se mostraran de color magenta")
        # Actualizar el selectorPanel ozy
        self.selectorPanelTile = Tile(graph.Characters[self.selectors[1].currentId]["character"], self.selectors[0].currentId, self.selectors[2].currentId, 1)
        self.selectorPanel.title = f"[{self.selectorPanelTile}{graph.ForeColors[self.selectorPanel.colorId]['color']}]Selectores"
        
        print2d.clear() # Lo que nunca hacer, ya bañate w
        
    # Sus nombres son parecidos, pero esta función añade un tile al selector de tiles
    # usando los valores del selector de valores, aunque le digo selectores    
    def changeTile(self):
        #Mucho texto
        self.tileSelector.change(graph.Characters[self.selectors[1].currentId]["character"], self.selectors[0].currentId, self.selectors[2].currentId, self.selectors[3].currentId)
        self.oh.add(self.tileSelector.tiles[self.tileSelector.currenTile].foreColorId)
        self.curse.colorId = self.tileSelector.tiles[self.tileSelector.currenTile].foreColorId
        bus.emit('state-change', states.States.DRAW) # Cambia el estado a DIBUJO cuando termina
    
    # Actualiza el cursor    
    def updateCurse(self, *args, **kwargs):
        self.curse.colorId = self.tileSelector.tiles[self.tileSelector.currenTile].foreColorId
    
    # Esta cosa hace que dibujes solo con mover el cursor    
    def fastDrawModeToogle(self):
        self.fastDrawMode = not self.fastDrawMode
        self.curse.curse = '☼' if self.fastDrawMode else '○'
        if self.fastDrawMode:
            self.drawTile()
            
    # Cuando dibujas, se ejecuta esta funcion    
    def fastDraw(self, *args, **kwargs):
        if self.fastDrawMode:
            self.drawTile()
            
    def renameLayer(self):
        states.isRendering = True
        self.showCMDCurse(True)
        self.lrmsgBox.position = Vector2(self.layermaster.margin.x - 22, self.layermaster.margin.y + self.layermaster.currentId - 3)
        makuka = self.lrmsgBox.getText('Renombrar capa', f'Ingrese un nuevo nombre para [{self.layermaster.layers[self.layermaster.currentId]["name"]}]',18)
        if makuka['state']:
            self.layermaster.layers[self.layermaster.currentId]['name'] = makuka['string']
            
        self.showCMDCurse(False)
        states.isRendering= False
        
    def clear(self):
        if self.msgBox.getYesNo('Limpiar Capa', 'Estás seguro de querer limpar la capa actual?'):
            self.layermaster.clear()
            
    def fill(self):
        self.layermaster.fill(self.curse.position.copy(), self.tileSelector.tiles[self.tileSelector.currenTile].copy())