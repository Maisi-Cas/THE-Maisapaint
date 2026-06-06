import engine.graph as graph

class Tile:
    def __init__(self, character, foreColorID, backColorID, styleID):
        self.character = character
        self.foreColorId = foreColorID
        self.backColorId = backColorID
        self.styleId = styleID
    
    def __str__(self):
        return graph.ForeColors[self.foreColorId]['color'] + graph.BackColors[self.backColorId]['color'] + graph.StyleType[self.styleId]['style'] + self.character + graph.Reset.STYLE
    
    def getString(self) -> str:
        return graph.ForeColors[self.foreColorId]['color'] + graph.BackColors[self.backColorId]['color'] + graph.StyleType[self.styleId]['style'] + self.character + graph.Reset.STYLE
    
    def copy(self):
        return Tile(self.character, self.foreColorId, self.backColorId, self.styleId)
    
    def getList(self):
        return [self.foreColorId, self.backColorId, self.styleId, self.character]