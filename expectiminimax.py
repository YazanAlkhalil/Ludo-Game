from state import State
from typing import Optional
from dataclasses import dataclass
import copy

@dataclass
class Move:
    piece: any
    steps: int
    score: float = 0.0

class Expectiminimax:
    def __init__(self, depth: int = 3):
        self.depth = depth
        self.max_score = float('inf')
        self.min_score = float('-inf')

    def find_best_move(self, state: Optional[State]) -> Optional[Move]:
        if not state:
            return None
            
        current_player = state.current_player
        valid_moves = self._get_valid_moves(state)
        
        if not valid_moves:
            return None
            
        best_move = None
        best_score = self.min_score
        
        for move in valid_moves:
            # Simulate move
            new_state = self._apply_move(state, move)
            score = self._expectiminimax(new_state, self.depth - 1, False)
            
            if score > best_score:
                best_score = score
                best_move = move
                
        return best_move
    
    def _expectiminimax(self, state: State, depth: int, is_max: bool) -> float:
        if depth == 0 or self._is_terminal(state):
            return self._evaluate(state)
            
        if is_max:
            return self._max_value(state, depth)
        else:
            return self._chance_value(state, depth)
    
    def _max_value(self, state: State, depth: int) -> float:
        valid_moves = self._get_valid_moves(state)
        if not valid_moves:
            return self._evaluate(state)
            
        value = self.min_score
        for move in valid_moves:
            new_state = self._apply_move(state, move)
            value = max(value, self._expectiminimax(new_state, depth - 1, False))
        return value
    
    def _chance_value(self, state: State, depth: int) -> float:
        # Simulate dice rolls
        total_value = 0
        for dice_value in range(1, 7):  # 1 to 6
            # Probability of each dice value is 1/6
            prob = 1.0 / 6.0
            new_state = self._apply_dice_roll(state, dice_value)
            value = self._expectiminimax(new_state, depth - 1, True)
            total_value += prob * value
        return total_value
    
    def _get_valid_moves(self, state: State) -> list[Move]:
        """Get all valid moves for current state"""
        valid_moves = []
        current_player = state.current_player
        if hasattr(state.board, 'get_valid_moves'):
            # Assuming dice value of 6 for now - this should be improved
            moves = state.board.get_valid_moves(current_player, state.dice_value)
            for piece, steps in moves:
                valid_moves.append(Move(piece=piece, steps=steps))
        return valid_moves
    
    def _apply_move(self, state: State, move: Move) -> State:
        """Apply move to state and return new state"""
        # Create a deep copy of the current state
        new_state = copy.deepcopy(state)
        
        # Find the piece in the new state
        new_piece = None
        for piece in new_state.current_player.pieces:
            if piece.number == move.piece.number:
                new_piece = piece
                break
        
        if new_piece:
            print(f"Applying move for piece {new_piece.number}: from pos={new_piece.position}")  # Debug print
            # Get the old position
            old_pos = new_piece.position
            
            # Remove piece from old position if it's on the board
            if old_pos != -1:
                old_cell = new_state.board.get_cell(old_pos)
                if old_cell and new_piece in old_cell.pieces:
                    old_cell.pieces.remove(new_piece)
            
            # Calculate new position
            next_pos = new_state.board.get_next_position(old_pos, move.steps, new_piece.color)
            print(f"Next position calculated: {next_pos}")  # Debug print
            
            # Add piece to new position if valid
            if next_pos != -1:
                new_cell = new_state.board.get_cell(next_pos)
                if new_cell:
                    # Handle capturing
                    if new_cell.pieces and new_cell.pieces[0].color != new_piece.color and not new_cell.is_safe:
                        captured_piece = new_cell.pieces[0]
                        captured_piece.position = -1
                        captured_piece.is_home = True
                        new_cell.pieces.clear()
                    
                    new_cell.pieces.append(new_piece)
                    new_piece.position = next_pos
                    new_piece.is_home = False
                    
                    # Check if piece reached end zone
                    path = new_state.board.paths[new_piece.color]
                    if next_pos == path['home_start'] + 5:
                        new_piece.is_done = True
            
            print(f"After move: piece {new_piece.number} at pos={new_piece.position}")  # Debug print
        
        return new_state
    
    def _is_terminal(self, state: State) -> bool:
        """Check if state is terminal (game over)"""
        return state.current_player.is_winning()
    
    def _evaluate(self, state: State) -> float:
        """Evaluate state and return score"""
        # Simple evaluation: count pieces in end zone
        score = 0
        current_player = state.current_player
        for piece in current_player.pieces:
            if piece.is_in_end_zone():
                score += 1
        return float(score)
    def _apply_dice_roll(self, state: State, dice_value: int) -> State:
        """Apply dice roll to state and return new state"""
        # Create a deep copy of the current state
        new_state = copy.deepcopy(state)
        
        # Set the dice value in the new state
        new_state.dice_value = dice_value
        
        # Update valid moves based on the new dice value
        valid_moves = self._get_valid_moves(new_state)
        new_state.valid_moves = valid_moves
        
        return new_state