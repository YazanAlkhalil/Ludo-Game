from color import Color

class Piece:
    def __init__(self, color: Color, number: int):
        self.color = color
        self.number = number
        self.position = -1
        self.is_home = True
        self.is_done = False
        
    def get_next_position(self, steps):
        if self.is_home:
            if steps == 6:
                return 0
            return -1
        
        next_pos = self.position + steps
        if next_pos < 56:
            return next_pos
        return -1
    
    def is_safe_at(self, position):
        if position == -1:              return True
        return False  
    
    def move(self, steps):
        next_pos = self.get_next_position(steps)
        if next_pos != -1:
            self.position = next_pos
            self.is_home = False
            return True
        return False
    
    
    def can_move(self, steps, board):
        if self.is_home:
            return steps == 6  
        
        next_pos = board.get_next_position(self.position, steps, self.color)
        if next_pos == -1:
            return False  
        
        target_cell = board.get_cell(next_pos)
        if not target_cell:
            return False
        
        current_pos = self.position
        while current_pos != next_pos:
            current_pos = board.get_next_position(current_pos, 1, self.color)
            cell = board.get_cell(current_pos)
            if cell and cell.is_wall():
                return cell.pieces[0].color == self.color

        
        return True  
    
    def is_in_end_zone(self):
        if self.is_done:
            return True
            
        end_zones = {
            Color.BLUE: range(52, 58),
            Color.RED: range(58, 64),
            Color.GREEN: range(64, 70),
            Color.YELLOW: range(70, 76)
        }
        
        return self.position in end_zones.get(self.color, [])
  