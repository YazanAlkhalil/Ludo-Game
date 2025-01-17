class MoveValidator:
    def __init__(self, board):
        self.board = board
    
    def validate_move(self, piece, steps, current_player):
        """Main validation method that checks all conditions"""
        if not self._can_leave_home(piece, steps):
            return False, None
            
        next_position = self._calculate_next_position(piece, steps)
        if next_position is None:
            return False, None
            
        capture_info = self._check_capture(next_position)
        return True, capture_info
    
    def _can_leave_home(self, piece, steps):
        """Check if piece can leave home base"""
        return not piece.is_home or steps == 6
    
    def _check_capture(self, position):
        """Check if move results in capturing opponent piece"""
        cell = self.board.get_cell(position)
        if not cell or not cell.pieces:
            return None
            
        target_piece = cell.pieces[0]
        if target_piece.color != self.current_player.color:
            return target_piece
        return None