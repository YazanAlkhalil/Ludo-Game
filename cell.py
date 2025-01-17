from color import Color

class Cell:
    def __init__(self, color: Color = None):
        self.color = color
        self.pieces = []
        self.is_safe = False
    
    def is_wall(self):
        """
        A wall is formed when:
        - Two or more pieces of the same color are on the cell
        - Cannot be crossed by opponent
        """
        if len(self.pieces) >= 2:
            return all(p.color == self.pieces[0].color for p in self.pieces)
        return False
    