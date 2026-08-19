# ruff: noqa: F841
from colorama import init, Fore, Style, Back

class _Reset:
    def __init__(self):
        self.STYLE = Style.RESET_ALL
        self.BACK = Back.RESET
        self.FORE = Fore.RESET
        

init()

ForeColors = {
    0: {'color': Fore.RED, 'light' : False},
    1: {'color': Fore.LIGHTRED_EX, 'light' : False},
    2: {'color': Fore.YELLOW, 'light' : False},
    3: {'color': Fore.LIGHTYELLOW_EX, 'light' : True},
    4: {'color': Fore.GREEN, 'light' : False},
    5: {'color': Fore.LIGHTGREEN_EX, 'light' : False},
    6: {'color': Fore.CYAN, 'light' : False},
    7: {'color': Fore.LIGHTCYAN_EX, 'light' : True},
    8: {'color': Fore.BLUE, 'light' : False},
    9: {'color': Fore.LIGHTBLUE_EX, 'light' : False},
    10: {'color': Fore.MAGENTA, 'light' : False},
    11: {'color': Fore.LIGHTMAGENTA_EX, 'light' : False},
    12: {'color': Fore.LIGHTWHITE_EX, 'light' : True},
    13: {'color': Fore.WHITE, 'light' : True},
    14: {'color': Fore.LIGHTBLACK_EX, 'light' : True},
    15: {'color': Fore.BLACK, 'light' : False}
}

BackColors = {
    0: {'color': Back.RED, 'light' : False},
    1: {'color': Back.LIGHTRED_EX, 'light' : False},
    2: {'color': Back.YELLOW},
    3: {'color': Back.LIGHTYELLOW_EX, 'light' : True},
    4: {'color': Back.GREEN, 'light' : False},
    5: {'color': Back.LIGHTGREEN_EX, 'light' : False},
    6: {'color': Back.CYAN, 'light' : False},
    7: {'color': Back.LIGHTCYAN_EX, 'light' : True},
    8: {'color': Back.BLUE, 'light' : False},
    9: {'color': Back.LIGHTBLUE_EX, 'light' : False},
    10: {'color': Back.MAGENTA, 'light' : False},
    11: {'color': Back.LIGHTMAGENTA_EX, 'light' : False},
    12: {'color': Back.LIGHTWHITE_EX, 'light' : True},
    13: {'color': Back.WHITE, 'light' : True},
    14: {'color': Back.LIGHTBLACK_EX, 'light' : True},
    15: {'color': Back.BLACK, 'light' : False}
}

Characters = {
    0: {'character': '@', 'customizable': False},
    1: {'character': '#', 'customizable': False},
    2: {'character': '%', 'customizable': False},
    3: {'character': '&', 'customizable': False},
    4: {'character': '$', 'customizable': False},
    5: {'character': '*', 'customizable': False},

    6: {'character': '+', 'customizable': False},
    7: {'character': '=', 'customizable': False},
    8: {'character': ';', 'customizable': False},
    9: {'character': ':', 'customizable': False},
    10: {'character': ',', 'customizable': False},
    11: {'character': '.', 'customizable': False},

    12: {'character': ' ', 'customizable': False},
    
    13: {'character': '░', 'customizable': False},
    14: {'character': '▒', 'customizable': False},
    15: {'character': '▓', 'customizable': False},
    16: {'character': '█', 'customizable': False},

    17: {'character': 'C', 'customizable': True},
    18: {'character': 'U', 'customizable': True},
    19: {'character': 'S', 'customizable': True},
    20: {'character': 'T', 'customizable': True},
    21: {'character': 'O', 'customizable': True},
    22: {'character': 'M', 'customizable': True},
    23: {'character': '1', 'customizable': True},
    24: {'character': '2', 'customizable': True}
}

StyleType = {
    0: {'name' : 'dim', 'style' : Style.DIM},
    1: {'name' : 'normal', 'style' : Style.NORMAL},
    2: {'name' : 'bright', 'style' : Style.BRIGHT}
}

def foreColor(id: int):
    id = min(max(0, id), 15)
    return ForeColors[id]['color']

def style(id: int):
    
    id = min(max(0, id), 2)
    return StyleType[0]['style']

Reset = _Reset()