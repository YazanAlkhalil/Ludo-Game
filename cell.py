from color import Color

class Cell:
    def __init__(self, color: Color = None):
        self.color = color
        self.pieces = []
        self.is_safe = False
    
    def is_wall(self):
        if len(self.pieces) >= 2:
            return all(p.color == self.pieces[0].color for p in self.pieces)
        return False
    