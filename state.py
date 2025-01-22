import copy

class State:
    def __init__(self, board, player, parent=None, dice_value=None):
        self.board = copy.deepcopy(board)
        self.current_player = copy.deepcopy(player)
        self.players = [
            copy.deepcopy(self.board.player1),
            copy.deepcopy(self.board.player2)
        ]
        self.dice_value = dice_value
        self.parent = parent  
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
    
    def apply_dice_roll(self, value: int) -> 'State':
        """Creates new state after dice roll"""
        new_state = copy.deepcopy(self)
        new_state.parent = self
        new_state.dice_value = value
        return new_state
    
    def apply_move(self, move) -> 'State':
        """Creates new state after applying move"""
        new_state = copy.deepcopy(self)
        new_state.parent = self
        captured = False
        
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
                        captured = True
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
            
        # Check consecutive sixes and update player turn
        if not captured and not self._should_keep_turn():
            new_state.switch_player()

        new_state.dice_value = None
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

    def _should_keep_turn(self) -> bool:
        """
        Determine if current player should keep their turn based on dice rolls
        Returns True if player keeps turn, False if turn should switch
        """
        if self.dice_value != 6:
            return False

        # Count consecutive sixes by traversing parent states
        consecutive_sixes = 1  # Count current six
        current = self
        while current.parent and consecutive_sixes < 3:
            if current.parent.dice_value == 6:
                consecutive_sixes += 1
            else:
                break
            current = current.parent

        return consecutive_sixes < 3

    def get_last_n_dice_values(self, n: int) -> list:
        """Get the last n dice values from state history"""
        values = []
        current = self
        while current and len(values) < n:
            if current.dice_value is not None:
                values.append(current.dice_value)
            current = current.parent
        return values

    def switch_player(self):
        """Switch to the other player"""
        self.current_player = (
            self._find_player_in_state(self.board.player2) 
            if self.current_player.color == self.board.player1.color 
            else self._find_player_in_state(self.board.player1)
        )

    def _find_player_in_state(self, original_player):
        """Find corresponding player in the current state"""
        for player in self.players:
            if player.color == original_player.color:
                return player
        return None

class StateManager:
    def __init__(self):
        self.states = []
    
    def save_state(self, state: State):
        """Save a state to the history"""
        self.states.append(state)
    
    def get_last_state(self) -> State:
        """Get the most recent state, or None if no states exist"""
        return self.states[-1] if self.states else None
    
    def clear_history(self):
        """Clear the state history"""
        self.states.clear()