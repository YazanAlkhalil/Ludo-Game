from color import Color

class Piece:
    def __init__(self, color: Color, number: int):
        self.color = color
        self.number = number
        self.position = -1  # -1 means in home base
        self.is_home = True
        self.is_done = False
        
    def get_next_position(self, steps):
        """Calculate next position after moving given steps"""
        if self.is_home:
            if steps == 6:
                return 0  # Start position
            return -1
        
        next_pos = self.position + steps
        if next_pos < 56:
            return next_pos
        return -1  # Invalid move
    
    def is_safe_at(self, position):
        """Check if piece would be safe at given position"""
        if position == -1:  # In home base
            return True
        return False  # سيتم التحقق من الأمان في Cell
    
    def move(self, steps):
        """Move piece by given steps"""
        next_pos = self.get_next_position(steps)
        if next_pos != -1:
            self.position = next_pos
            self.is_home = False
            return True
        return False
    
    
    def can_move(self, steps, board):
        """Check if piece can move given steps"""
        if self.is_home:
            return steps == 6
        
        next_pos = board.get_next_position(self.position, steps, self.color)
        if next_pos == -1:
            return False
        
        # Allow movement into home path (positions >= 52)
        if next_pos >= 52:
            return True
        
        target_cell = board.get_cell(next_pos)
        return target_cell and target_cell.can_move_to(self)
  