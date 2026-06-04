# Clases del motor
from engine.panel import Panel
import engine.graph as graph

# Clases del nucleo
import core.states as states
from core.inputHandler import Input

# Clases utiles
from utils.vector2 import Vector2
from utils.print2d import Print2D as print2d

# Clases de la ui
from ui.textBox import TextBox 

class MsgBox:
    def __init__(self, position: Vector2, colorId):
        self.input = Input()
        self.colorId = colorId
        self.position = position.copy()
        
    def get(self, title: str,content: str):
        states.isMsgBoxOn = True
        txtBox = TextBox(self.position + 1, Vector2(20,10), content, 12)
        michaelJackson = (len(content) // txtBox.size.x) + 2
        michaelJackson += 1 if len(content) % txtBox.size.x  != 0 else 0
        
        panel = Panel(title, self.colorId, self.position - 1, Vector2(20, michaelJackson))
        
        while(True):
            if not states.clockIsRendering:
                panel.render(True)
                txtBox.render()
                print2d.coord(self.position.x + 1, self.position.y + michaelJackson , f"[{graph.ForeColors[4]['color']}J{graph.Reset.STYLE}] OK")
                if self.input.get() == 'accept':
                    print2d.clear()
                    break
            else:
                pass
        
        states.isMsgBoxOn = False
            
    def getYesNo(self, title: str, content: str):
        states.isMsgBoxOn = True
        txtBox = TextBox(self.position + 1, Vector2(20,10), content, 12)
        michaelJackson = (len(content) // txtBox.size.x) + 3
        michaelJackson += 1 if len(content) % txtBox.size.x  != 0 else 0
        
        panel = Panel(title, self.colorId, self.position - 1, Vector2(20, michaelJackson))
        
        while(True):
            if not states.clockIsRendering:
                panel.render(True)
                txtBox.render()
                print2d.coord(self.position.x + 1, self.position.y + michaelJackson - 1, f"[{graph.ForeColors[4]['color']}J{graph.Reset.STYLE}] SI")
                print2d.coord(self.position.x + 1, self.position.y + michaelJackson , f"[{graph.ForeColors[0]['color']}K{graph.Reset.STYLE}] NO")
                key = self.input.get()
                match key:
                    case 'accept':
                        print2d.clear()
                        states.isMsgBoxOn = False
                        return True
                    case 'cancel':
                        print2d.clear()
                        states.isMsgBoxOn = False
                        return False
                    case _:
                        pass
            else:
                pass
    
    def getText(self, title:str, content:str, size: int = 10) -> dict[bool,str]:
    
        size = 18 if size > 18 else size
        size = 1 if size < 1 else size
        
        states.isMsgBoxOn = True
        txtBox = TextBox(self.position + 1, Vector2(20,10), content, 12)
        michaelJackson = (len(content) // txtBox.size.x) + 7
        michaelJackson += 1 if len(content) % txtBox.size.x  != 0 else 0
        status = {
                    'state' : False,
                    'string' : '...'
                }
        panel = Panel(title, self.colorId, self.position - 1, Vector2(20, michaelJackson))
        spanel = Panel('', 12, Vector2(self.position.x + ((20 - (size + 2)) // 2), self.position.y + michaelJackson - 6), Vector2(size, 1))
        cursePos = Vector2(self.position.x + 2 + ((20 - (size + 2)) // 2), self.position.y + michaelJackson - 4)
        while(True):
            if not states.clockIsRendering:
                
                panel.render(True)
                txtBox.render()
                spanel.render()
                print2d.coord(cursePos.x, cursePos.y, status['string'])
                print2d.coord(self.position.x + 1, self.position.y + michaelJackson - 2, f"[{graph.ForeColors[4]['color']}J{graph.Reset.STYLE}] ACEPTAR")
                print2d.coord(self.position.x + 1, self.position.y + michaelJackson - 1, f"[{graph.ForeColors[2]['color']}I{graph.Reset.STYLE}] EDITAR")
                print2d.coord(self.position.x + 1, self.position.y + michaelJackson , f"[{graph.ForeColors[0]['color']}K{graph.Reset.STYLE}] CANCELAR")
                key = self.input.get()
                match key:
                    case 'accept':
                        status['state'] = True
                        break
                    case 'cancel':
                        status['state'] = False
                        break
                    case 'extra-0':
                        print2d.coord(cursePos.x, cursePos.y, " " * size)
                        print2d.cursePos(cursePos.x, cursePos.y)
                        string = input()
                        if len(string) > size:
                            string = string[:size]
                        status['string'] = string
                    case _:
                        pass
            else:
                pass
        
        print2d.clear()
        return status