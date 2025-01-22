from state import State
from player import Player
from typing import Optional
from dataclasses import dataclass
import copy
from enum import Enum

@dataclass
class Move:
    piece: any
    steps: int
    score: float = 0.0

class NodeType(Enum):
    MAX = 1
    MIN = 2
    CHANCE = 3

class Expectiminimax:
    def __init__(self, depth: int = 3, player: Player = None):
        self.depth = depth
        self.max_score = float('inf')
        self.min_score = float('-inf')
        self.player = player

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
            score = self._expectiminimax(new_state, self.depth - 1, NodeType.CHANCE)
            
            if score > best_score:
                best_score = score
                best_move = move
                
        return best_move
    
    def _expectiminimax(self, state: State, depth: int, node_type: NodeType) -> float:
        indent = "  " * (self.depth - depth)  # For prettier printing
        
        if depth == 0 or state.is_terminal():
            value = self._evaluate(state)
            print(f"{indent}LEAF NODE (depth={depth}): {value}")
            return value
            
        if node_type == NodeType.MAX:
            print(f"{indent}MAX NODE (depth={depth}, player={state.current_player.color})")
            return self._max_value(state, depth, indent)
        
        elif node_type == NodeType.MIN:
            print(f"{indent}MIN NODE (depth={depth}, player={state.current_player.color})")
            return self._min_value(state, depth, indent)
        
        elif node_type == NodeType.CHANCE:
            print(f"{indent}CHANCE NODE (depth={depth})")
            return self._chance_value(state, depth, indent)
    
    def _max_value(self, state: State, depth: int, indent: str) -> float:
        valid_moves = state.get_valid_moves()
        if not valid_moves:
            value = self._evaluate(state)
            print(f"{indent}NO MOVES AVAILABLE: {value}")
            return value
            
        values = []
        for piece, steps in valid_moves:
            new_state = state.apply_move(Move(piece, steps))
            # After player move, it's a chance node
            value = self._expectiminimax(new_state, depth - 1, NodeType.CHANCE)
            values.append(value)
            print(f"{indent}Move piece {piece.number} by {steps} steps -> value: {value}")
        
        best_value = max(values)
        print(f"{indent}MAX chose: {best_value}")
        return best_value
    
    def _min_value(self, state: State, depth: int, indent: str) -> float:
        valid_moves = state.get_valid_moves()
        if not valid_moves:
            value = self._evaluate(state)
            print(f"{indent}NO MOVES AVAILABLE: {value}")
            return value
            
        values = []
        for piece, steps in valid_moves:
            new_state = state.apply_move(Move(piece, steps))
            # After opponent move, it's a chance node
            value = self._expectiminimax(new_state, depth - 1, NodeType.CHANCE)
            values.append(value)
            print(f"{indent}Move piece {piece.number} by {steps} steps -> value: {value}")
        
        worst_value = min(values)
        print(f"{indent}MIN chose: {worst_value}")
        return worst_value
    
    def _chance_value(self, state: State, depth: int, indent: str) -> float:
        total_value = 0
        print(f"{indent}Rolling dice (1-6):")
        
        for dice_value in range(1, 7):
            probability = 1/6
            new_state = state.apply_dice_roll(dice_value)
            
            # Check if it's still the same player's turn based on dice value and history
            is_same_player = dice_value == 6 and not new_state._should_keep_turn()
            next_node_type = NodeType.MAX if (
                (is_same_player and new_state.current_player.color == self.player.color) or
                (not is_same_player and new_state.current_player.color != self.player.color)
            ) else NodeType.MIN
            
            value = self._expectiminimax(new_state, depth - 1, next_node_type)
            expected_value = value * probability
            total_value += expected_value
            print(f"{indent}Dice={dice_value}: value={value}, prob=1/6, expected={expected_value:.2f}")
        
        print(f"{indent}CHANCE expected value: {total_value:.2f}")
        return total_value
    
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

  