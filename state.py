import copy

class State:
    def __init__(self, board, player):
        self.board = copy.deepcopy(board)
        self.current_player = copy.deepcopy(player)
        self.players = [
            copy.deepcopy(self.board.player1),
            copy.deepcopy(self.board.player2)
        ]
        
        self.dice_value = None
        
        self._sync_pieces_with_board()
    
    def _sync_pieces_with_board(self):
        """Ensure pieces in cells reference the copied pieces"""
        # First clear all cells
        for cell in self.board.cells:
            cell.pieces = []
            
        # Then add pieces back to their correct positions
        for player in self.players:
            for piece in player.pieces:
                if piece.position != -1:
                    cell = self.board.get_cell(piece.position)
                    if cell:
                        cell.pieces.append(piece)
    
    def apply_move(self, move) -> 'State':
        """Creates new state after applying move"""
        new_state = copy.deepcopy(self)
        
        # Find the piece in the new state
        piece = self._find_piece_in_new_state(new_state, move.piece)
        if piece:
            # First remove the piece from its current cell
            if piece.position != -1:
                old_cell = new_state.board.get_cell(piece.position)
                if old_cell:
                    # Remove by matching piece number and color instead of reference
                    old_cell.pieces = [p for p in old_cell.pieces 
                                     if p.number != piece.number or p.color != piece.color]
            
            # Calculate new position
            next_pos = new_state.board.get_next_position(piece.position, move.steps, piece.color)
            if next_pos != -1:
                new_cell = new_state.board.get_cell(next_pos)
                if new_cell:
                    # Handle capturing
                    if new_cell.pieces and new_cell.pieces[0].color != piece.color and not new_cell.is_safe:
                        captured_piece = new_cell.pieces[0]
                        captured_piece.position = -1
                        captured_piece.is_home = True
                        new_cell.pieces.clear()
                    
                    # Add piece to new position
                    new_cell.pieces.append(piece)
                    piece.position = next_pos
                    piece.is_home = False
                    
                    # Check if piece reached end zone
                    path = new_state.board.paths[piece.color]
                    if next_pos == path['home_start'] + 5:
                        piece.is_done = True
            
        new_state.dice_value = None
        return new_state
    
    def apply_dice_roll(self, value: int) -> 'State':
        """Creates new state after dice roll"""
        new_state = copy.deepcopy(self)
        new_state.dice_value = value
        return new_state
    
    def get_valid_moves(self) -> list:
        """Returns valid moves for current state"""
        return self.board.get_valid_moves(self.current_player, self.dice_value)
    
    def is_terminal(self) -> bool:
        """Checks if state is terminal"""
        return self.current_player.is_winning()
    
    def _find_piece_in_new_state(self, new_state, original_piece):
        """Find corresponding piece in new state"""
        for piece in new_state.current_player.pieces:
            if piece.number == original_piece.number:
                return piece
        return None

class StateManager:
    def __init__(self):
        self.states = []
        
    def create_state(self, board, player):
        """Create a new state from the given information"""
        
        new_state = State(
            board=board,
            player=player,
            
        )
        return new_state
    
    def save_state(self, board, player):
        """Create and save a new state"""
        new_state = self.create_state(board, player)
        self.states.append(new_state)
        return new_state
    
    def get_last_state(self):
        """Get the most recent state"""
        return self.states[-1] if self.states else None
    
    def clear_states(self):
        """Clear all saved states"""
        self.states = []