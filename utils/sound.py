import pygame

# Clases utiles
from utils.vector2 import Vector2
from utils.print2d import Print2D as print2d

# Clases del motor
import engine.graph as graph 

# Clases del nucleo
from core.emitBus import bus

class Audio:
    def __init__(self):
        pygame.mixer.init()
        
        self.sounds = {
            'clear' : pygame.mixer.Sound('sounds/clear.wav'),
            'states' : pygame.mixer.Sound('sounds/states.wav'),
            'ambient' : pygame.mixer.Sound('sounds/ambient.wav'),
            'click-1' : pygame.mixer.Sound('sounds/click-1.wav'),
            'click-2' : pygame.mixer.Sound('sounds/click-2.wav')
        }
        self.volume = 1
        self.position = Vector2(1,1)
        
        bus.conect('volume', self.addVolume)
    
    def play(self, key: str):
        return
        if key in self.sounds.keys():
            self.sounds[key].set_volume(self.volume)
            self.sounds[key].play()
            
    def repeat(self, key: str):
        return
        if key in self.sounds.keys():
            self.sounds[key].set_volume(self.volume)
            self.sounds[key].play(-1)
            
    def stop(self, key: str):
        return
        if key in self.sounds.keys():
            self.sounds[key].stop()
            
    def addVolume(self, boo: bool):
        return
        
        if boo:
            self.volume += 0.1
        else :
            self.volume -= 0.1
            
        self.volume = max(0, min(self.volume, 1))
        
        for i in self.sounds.values():
            i.set_volume(self.volume)
            
    def setPos(self, position: Vector2):
        return
        self.position = position.copy()
        
    def render(self):
        return
        num = max(0, min(2, ((self.volume * 10) // 3) - 1))
        
        barstring = ""
        barstring += graph.StyleType[num]['style']
        for i in range(10):
            if ((i +1 ) * 0.1) <= self.volume:
                barstring += "#"
            else:
                barstring += " "
        barstring += graph.Reset.STYLE 
        
        print2d.coord(self.position.x, self.position.y, f'VOLUME[{barstring}]')