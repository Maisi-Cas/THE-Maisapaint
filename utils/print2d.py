import os
import msvcrt
from utils.vector2 import Vector2
from abc import ABC, abstractclassmethod


class Print2D(ABC):
    
    def coord(x: int = 1, y: int  = 1, string: str = 'Lorem Ipsum!', flush: bool = False):
        if x <= 0 or y <= 0:
            return
        print(f"\033[{y};{x}H{string}", flush=flush)
        
    def cursePos(x: int = 1, y: int = 1):
        if x <= 0 or y <= 0:
            return
        print(f"\033[{y};{x}H", end='')
        
    def clear():
        print('\033[2J\033[H', end='', flush=True)
        
    def debugPrint(string: str):
        os.system('cls')
        print(string)
        msvcrt.getch()
        
    def synapsis(self, a: Vector2, b:Vector2, colorId: int):
        colorId = max(0, min(15, colorId))

        # No se como ejecutar mi idea, pero se que puedo
        # Mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
        
        # A ver hijo de la grandiosa, ponte System.out.println("HelloWorld");
        # Primero debemos ver la diferencia que tenemos
        
        delta: Vector2 = b - a
        
        for i in range(delta.x + 1):
            self.coord()

    def getStr(x, y):
        x = max(1,x)
        y = max(1,y)

        return f"\033[{y};{x}H"
