import numbers

class Vector2:
    def __init__(self, x: numbers.Number, y: numbers.Number):
        self.x = x
        self.y = y
        
    # Comparación
    
    def __eq__(self, value):
        if not isinstance(value, Vector2):
            return False
        return self.x == value.x and self.y == value.y
    
    def __hash__(self):
        hash((self.x, self.y))
        
    # region Operaciones aritmeticas
    
    def __add__(self, other):
        if isinstance(other, numbers.Number):
            return Vector2(self.x + other, self.y + other)
        elif isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        else:
            return other
        
    def __sub__(self, other):
        if isinstance(other, numbers.Number):
            return Vector2(self.x - other, self.y - other)
        elif isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        else:
            return other
        
    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            return Vector2(self.x * other, self.y * other)
        elif isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        else:
            return other
        
    def __floordiv__(self, other):
        if isinstance(other, numbers.Number):
            return Vector2(self.x // other, self.y // other)
        elif isinstance(other, Vector2):
            return Vector2(self.x // other.x, self.y // other.y)
        else:
            return other

    # endregion
    # region Operaciones in place
    
    def __iadd__(self, other):
        if isinstance(other, numbers.Number):
            self.x += other
            self.y += other
            return self
        elif isinstance(other, Vector2):
            self.x += other.x
            self.y += other.y
            return self
            
    def __isub__(self, other):
        if isinstance(other, numbers.Number):
            self.x -= other
            self.y -= other
            return self
        elif isinstance(other, Vector2):
            self.x -= other.x
            self.y -= other.y
            return self
            
    def __imul__(self, other):
        if isinstance(other, numbers.Number):
            self.x *= other
            self.y *= other
            return self
        elif isinstance(other, Vector2):
            self.x *= other.x
            self.y *= other.y
            return self
            
    def __ifloordiv__(self, other):
        if isinstance(other, numbers.Number):
            self.x //= other
            self.y //= other
            return self
        elif isinstance(other, Vector2):
            self.x //= other.x
            self.y //= other.y
            return self
        
    
    # endregion
    # region Cosillas
    
    def __str__(self):
        return f"({self.x}, {self.y})"
        
    def copy(self):
        return Vector2(self.x, self.y)
    
    def set(self, x:int, y:int):
        self.x, self.y = x, y
    
    # endregion