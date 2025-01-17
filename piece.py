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
        """
        Check if piece can make a valid move given the steps.
        
        Args:
            steps (int): Number of steps to move
            board: Game board instance
        
        Returns:
            bool: True if move is valid, False otherwise
        """
        # Case 1: Piece is in home base
        if self.is_home:
            return steps == 6  
        
        # Case 2: Calculate next position
        next_pos = board.get_next_position(self.position, steps, self.color)
        if next_pos == -1:
            return False  
        
        # Get target cell
        target_cell = board.get_cell(next_pos)
        if not target_cell:
            return False
        
        # Case 3: Check if any cell in path has a wall
        current_pos = self.position
        while current_pos < next_pos:
            current_pos += 1
            cell = board.get_cell(current_pos)
            if cell and cell.is_wall() and current_pos <= 51:
                return False
                
        # Check target cell wall
        if target_cell.is_wall():
            return target_cell.pieces[0].color == self.color
        
        # Case 4: Check if target is a safe zone with opponent
        if target_cell.is_safe and target_cell.pieces and not target_cell.is_wall():
            return True  

        
        
        
        return True  # All other cases are valid moves
  