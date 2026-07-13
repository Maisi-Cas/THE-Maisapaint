from engine.panel import Panel
from utils.vector2 import Vector2
from utils.print2d import Print2D as print2d
import threading
import time
from datetime import datetime
import engine.graph as graph
from core.emitBus import bus
import core.states as states


class Clock:
    def __init__(self, position: Vector2):
        self.position: Vector2 = position.copy()
        
        self.panel = Panel('TIME', 14, Vector2(self.position.x - 2, self.position.y - 2), Vector2(5,1), 1)

        self.isVisible = True
        self.running = True
        bus.conect('clock-visible', self.toogleVisibility)

        self.thread = threading.Thread(target=self.loop)
        self.thread.daemon = True
        self.thread.start()

    def toogleVisibility(self, value: bool):
        self.isVisible = value
    
    def render(self):
        hour = datetime.now().strftime("%H:%M")
        
        self.panel.render()
        print2d.coord(self.position.x, self.position.y, graph.ForeColors[5]['color'] + hour + graph.Reset.STYLE)
        

    def loop(self):
        while self.running:
            if self.isVisible and not states.isRendering:
                states.clockIsRendering = True
                self.render()
                states.clockIsRendering = False

            time.sleep(3)