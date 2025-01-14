from cell import Cell
from color import Color

class Path:
    def __init__(self, color: Color):
        self.color = color
        # Main track (52 cells) + home path (6 cells)
        self.cells = [Cell(Color.WHITE) for _ in range(58)]
        self.start_position = self._get_start_position()
        self.home_entrance = (self.start_position + 50) % 52  # Position before home path
        self._initialize_path()
    
    def _get_start_position(self):
        """Define starting position for each color on the main track"""
        start_positions = {
            Color.BLUE: 0,
            Color.RED: 13,
            Color.GREEN: 26,
            Color.YELLOW: 39
        }
        return start_positions.get(self.color, 0)
    
    def _initialize_path(self):
        # Initialize safe spots on main track
        
        # Initialize home path (last 6 cells)
        for i in range(52, 58):
            self.cells[i].color = self.color
            self.cells[i].is_safe = True
    
    def get_global_index(self, local_index):
        """Convert local index to global index"""
        if local_index >= 52:  # If in home path
            return local_index
        
        if local_index < 0:  # If in home base (not on board yet)
            return -1
            
        global_index = (self.start_position + local_index) % 52
        return global_index
    
    def get_local_index(self, global_index):
        """Convert global index to local index"""
        if global_index >= 52:  # If in home path
            return global_index
            
        if global_index < 0:  # If in home base
            return -1
            
        local_index = (global_index - self.start_position) % 52
        return local_index
    
    def is_home_entrance(self, global_index):
        """Check if position is at home path entrance"""
        return global_index == self.home_entrance
    
    def can_enter_home(self, from_index, steps):
        """Check if piece can enter home path"""
        local_index = self.get_local_index(from_index)
        target_index = local_index + steps
        
        # Check if piece will cross or land on home entrance
        return local_index < 50 and target_index >= 50
    
    def get_deepest_available_home_spot(self):
        """Find the deepest available spot in home path"""
        for i in range(57, 51, -1):  # Check from end to start of home path
            if not self.cells[i].has_piece():
                return i
        return None