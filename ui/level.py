# Clases utiles
from utils.vector2 import Vector2
from utils.print2d import Print2D

# Clases del motor
import engine.graph as graph

# Clases del nucleo
from core.emitBus import bus
import core.polla as polla

# graph.foreColor(self.countTiles() % 15) + str(self.countTiles()) + graph.Reset.STYLE

class Level:

    def __init__(self, position: Vector2):
        self.EEE = 20
        self.MAXLEVEL = 500

        self.xp = 0
        self.lvl = 499
        self.position = position.copy()
        bus.conect("add-xp", self.addXp)

    def setXp(self, xp):
        self.xp = xp

    def setLvl(self, lvl):
        self.lvl = lvl

    def addXp(self, xp):
        self.lvl = min(max(1, self.lvl), self.MAXLEVEL)
        if self.lvl >= self.MAXLEVEL:
            return
        
        self.xp += xp

        while self.xp >= self.reqXp():
            self.xp -= self.reqXp()
            self.lvl += 1
            if self.lvl >= self.MAXLEVEL:
                self.xp = 0
                return

    def reqXp(self):
        return int((self.EEE * (1 + (self.lvl * 0.5))))

    def render(self):
        sucoVI = lambda : "0" * (len(str(self.MAXLEVEL)) - len(str(self.lvl)))
        sucoVII = lambda : self.lvl if self.lvl < self.MAXLEVEL else "MAX"
        sucoVIII = lambda string : string if self.lvl < self.MAXLEVEL else polla.gayficationString(string)
        elAnoDeMaxi = round((self.xp / self.reqXp() * 2) * 10)
        barStr = ""

        for i in range(20):
            if i + 1 <= elAnoDeMaxi:
                barStr += f"{graph.backColor((self.lvl + 1) % 12)} {graph.Reset.STYLE}"
            else:
                barStr += " "

        barStr += graph.Reset.STYLE

        Print2D.coord(self.position.x, self.position.y, f"{graph.foreColor(self.lvl % 12)}{sucoVIII(f"LVL.{sucoVI()}{sucoVII()}")}{graph.Reset.STYLE}[{barStr}]")