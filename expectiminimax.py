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

    def find_best_move(self, state: State) -> Optional[Move]:
        if not state:
            return None
            
        valid_moves = state.get_valid_moves()
        if not valid_moves:
            return None
            
        best_move = None
        best_score = self.min_score
        
        for piece, steps in valid_moves:
            move = Move(piece=piece, steps=steps)
            new_state = state.apply_move(move)
            score = self._expectiminimax(new_state, self.depth - 1, False)
            
            if score > best_score:
                best_score = score
                best_move = move
                
        return best_move
    
    def _expectiminimax(self, state: State, depth: int, is_max: bool) -> float:
        if depth == 0 or state.is_terminal():
            return self._evaluate(state)
            
        if is_max:
            return self._max_value(state, depth)
        else:
            return self._chance_value(state, depth)
    
    def _max_value(self, state: State, depth: int) -> float:
        valid_moves = state.get_valid_moves()
        if not valid_moves:
            return self._evaluate(state)
            
        return max(
            self._expectiminimax(state.apply_move(Move(piece, steps)), depth - 1, False)
            for piece, steps in valid_moves
        )
    
    def _chance_value(self, state: State, depth: int) -> float:
        return sum(
            (1.0/6.0) * self._expectiminimax(state.apply_dice_roll(dice_value), depth - 1, True)
            for dice_value in range(1, 7)
        )
    
    def _evaluate(self, state: State) -> float:
        """Evaluate state and return score based on multiple factors"""
        score = 0.0
        current_player = state.current_player
        
        # Weight factors
        PIECE_VALUE = 10.0
        DISTANCE_WEIGHT = 0.5
        SAFETY_BONUS = 5.0
        WINNING_BONUS = 1000.0
        HOME_PENALTY = -2.0
        
        # Check for winning state
        if current_player.is_winning():
            return WINNING_BONUS
            
        for piece in current_player.pieces:
            # Base points for pieces in end zone
            if piece.is_done:
                score += PIECE_VALUE
                continue
                
            # Penalty for pieces still at home
            if piece.is_home:
                score += HOME_PENALTY
                continue
                
            # Calculate progress along path
            path = state.board.paths[piece.color]
            total_distance = path['home_start'] + 6  # Including end zone
            current_distance = piece.position
            if current_distance > 0:  # Only for pieces on board
                progress = current_distance / total_distance
                score += DISTANCE_WEIGHT * progress * PIECE_VALUE
            
            # Bonus for pieces in safe spots
            cell = state.board.get_cell(piece.position)
            if cell and cell.is_safe:
                score += SAFETY_BONUS
                
            # Consider threats from opponents
            threat_penalty = self._calculate_threats(state, piece)
            score -= threat_penalty
            
        return score

    def _calculate_threats(self, state: State, piece: any) -> float:
        """Calculate threat level for a given piece"""
        THREAT_WEIGHT = 3.0
        threat_score = 0.0
        
        if piece.is_home or piece.is_done:
            return 0.0
            
        # Get all opponent pieces
        for player in state.players:
            if player != state.current_player:
                for opp_piece in player.pieces:
                    if not opp_piece.is_home and not opp_piece.is_done:
                        # Calculate distance to opponent piece
                        distance = abs(piece.position - opp_piece.position)
                        if distance <= 6:  # Maximum dice roll
                            threat_score += (6 - distance) * THREAT_WEIGHT
        
        return threat_score

  