class MoveResult:
    def __init__(self):
        self.is_valid = False
        self.captured_piece = None
        self.extra_turn = False
        self.is_winning_move = False

class MoveHandler:
    def __init__(self, board, validator):
        self.board = board
        self.validator = validator
    
    def execute_move(self, piece, steps, current_player) -> MoveResult:
        result = MoveResult()
        
        is_valid, capture_info = self.validator.validate_move(piece, steps, current_player)
        if not is_valid:
            return result
            
        result.is_valid = True
        result.captured_piece = capture_info
        
        # Handle capture
        if capture_info:
            self._handle_capture(capture_info)
            result.extra_turn = True
        
        # Handle six
        if steps == 6:
            result.extra_turn = True
            
        return result
