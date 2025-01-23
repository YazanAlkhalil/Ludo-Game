from dice import Dice
from piece import Piece
from state import State
from player import Player
from typing import Optional, List, Tuple
from dataclasses import dataclass
import copy
from enum import Enum

@dataclass(frozen=True)
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
        self.dice = Dice()
        self.nodes_visited = 0
        self.max_nodes = 0
        self.min_nodes = 0
        self.chance_nodes = 0
        self.leaf_nodes = 0
        self.MAX_SCORE = 100000.0
        self.MIN_SCORE = -100000.0
        self.max_score = float('inf')
        self.min_score = float('-inf')
        self.player = player
        self.indent = 0
        self.verbose = False
        self.node_details = []

    def _get_indent(self) -> str:
        return "  " * self.indent

    def _reset_counters(self):
        self.nodes_visited = 0
        self.max_nodes = 0
        self.min_nodes = 0
        self.chance_nodes = 0
        self.leaf_nodes = 0

    def find_best_move(self, state: State) -> Optional[Move]:
        dice_history = state.get_last_n_dice_values(3)
        dice_history.reverse()
        
        print("\n=== Current Game State ===")
        print(f"Current roll: {state.dice_value}")
        if dice_history:
            print(f"Roll sequence: {' → '.join(str(x) for x in dice_history + [state.dice_value])}")
        
        print("\n=== Piece Positions ===")
        for piece in state.current_player.pieces:
            position_type = "Home" if piece.is_home else "Done" if piece.is_done else str(piece.position)
            cell = state.board.get_cell(piece.position) if not piece.is_home and not piece.is_done else None
            safety_status = "Safe" if cell and cell.is_safe else "Vulnerable"
            
            print(f"Piece {piece.number}: {position_type} ({safety_status})")
        
        self._reset_counters()
        
        valid_moves = state.get_valid_moves()
        if not valid_moves:
            print("\n=== Search Statistics ===")
            print("No valid moves available")
            print(f"Nodes visited: {self.nodes_visited}")
            return None
        
        print("\n=== Move Analysis ===")
        move_scores = {}
        for piece, steps in self._order_moves(valid_moves):
            move = Move(piece=piece, steps=steps)
            new_state = state.apply_move(move)
            score = self._expectiminimax(new_state, self.depth - 1, NodeType.CHANCE, 
                                       self.MIN_SCORE, self.MAX_SCORE)
            move_scores[move] = score
            
            next_pos = state.board.get_next_position(piece.position, steps, piece.color)
            target_cell = state.board.get_cell(next_pos)
            
            print(f"\nMove Option: Piece {piece.number} → {steps} steps")
            print(f"  Position: {piece.position if not piece.is_home else 'Home'} → {next_pos}")
            print(f"  Score: {score:.2f}")
            
            if piece.is_home and steps == 6:
                print("  Strategy: Getting new piece out")
            elif target_cell:
                if target_cell.is_safe:
                    print("  Strategy: Moving to safe spot")
                if target_cell.pieces and target_cell.pieces[0].color != piece.color:
                    print("  Strategy: Capture opportunity")
                
                threats = []
                for opp_piece in state.opponent.pieces:
                    if not opp_piece.is_home and not opp_piece.is_done:
                        distance = (opp_piece.position - next_pos) % 52
                        if 1 <= distance <= 6:
                            threats.append(f"Piece {opp_piece.number} at distance {distance}")
                if threats:
                    print(f"  Risks: Threatened by {', '.join(threats)}")
        
        best_move = max(move_scores.items(), key=lambda x: x[1])[0]
        print("\n=== Selected Move ===")
        print(f"Moving Piece {best_move.piece.number} by {best_move.steps} steps")
        print(f"Expected Value: {move_scores[best_move]:.2f}")
        
        print("\n=== Search Statistics ===")
        print(f"Total nodes visited: {self.nodes_visited}")
        print(f"├── MAX nodes: {self.max_nodes}")
        print(f"├── MIN nodes: {self.min_nodes}")
        print(f"├── CHANCE nodes: {self.chance_nodes}")
        print(f"└── Leaf nodes: {self.leaf_nodes}")
        print(f"\nSearch depth: {self.depth}")
        print(f"Best move score: {move_scores[best_move]:.2f}")
        
        return best_move
    
    def _order_moves(self, moves: List[Tuple['Piece', int]]) -> List[Tuple['Piece', int]]:
        def move_score(move):
            piece, steps = move
            if piece.is_done:
                return -1
            if piece.is_home and steps == 6:
                return 100
            if piece.position + steps >= 56:
                return 90
            return 56 - (piece.position + steps)
            
        return sorted(moves, key=move_score, reverse=True)
    
    def _expectiminimax(self, state: State, depth: int, node_type: NodeType, 
                       alpha: float, beta: float) -> float:
        self.nodes_visited += 1
        
        if alpha < self.MIN_SCORE:
            alpha = self.MIN_SCORE
        if beta > self.MAX_SCORE:
            beta = self.MAX_SCORE
            
        if depth == 0 or state.current_player.is_winning():
            self.leaf_nodes += 1
            score = state.evaluate()
            return max(min(score, self.MAX_SCORE), self.MIN_SCORE)
            
        if node_type == NodeType.MAX:
            self.max_nodes += 1
            value = self.MIN_SCORE
            valid_moves = state.get_valid_moves()
            for piece, steps in valid_moves:
                move = Move(piece=piece, steps=steps)
                new_state = state.apply_move(move)
                score = self._expectiminimax(new_state, depth - 1, NodeType.CHANCE, 
                                           alpha, beta)
                value = max(value, score)
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return value
            
        elif node_type == NodeType.MIN:
            self.min_nodes += 1
            value = self.MAX_SCORE
            valid_moves = state.get_valid_moves()
            for piece, steps in valid_moves:
                move = Move(piece=piece, steps=steps)
                new_state = state.apply_move(move)
                score = self._expectiminimax(new_state, depth - 1, NodeType.CHANCE, 
                                           alpha, beta)
                value = min(value, score)
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value
            
        else:
            self.chance_nodes += 1
            value = 0.0
            probabilities = self.dice.get_probabilities(state.get_last_n_dice_values(2))
            for dice_value, prob in probabilities.items():
                new_state = copy.deepcopy(state)
                new_state.dice_value = dice_value
                score = self._expectiminimax(new_state, depth - 1, 
                                           NodeType.MAX if dice_value == 6 else NodeType.MIN,
                                           alpha, beta)
                value += prob * score
            return max(min(value, self.MAX_SCORE), self.MIN_SCORE)
    
    def _evaluate(self, state: State) -> float:
        score = 0.0
        current_player = state.current_player
        PIECE_VALUE = 10.0
        DISTANCE_WEIGHT = 0.5
        SAFETY_BONUS = 5.0
        WINNING_BONUS = 1000.0
        HOME_PENALTY = -2.0
        
        if current_player.is_winning():
            return WINNING_BONUS
            
        for piece in current_player.pieces:
            if piece.is_done:
                score += PIECE_VALUE
                continue
                
            if piece.is_home:
                score += HOME_PENALTY
                continue
                
            path = state.board.paths[piece.color]
            total_distance = path['home_start'] + 6
            current_distance = piece.position
            if current_distance > 0:
                progress = current_distance / total_distance
                score += DISTANCE_WEIGHT * progress * PIECE_VALUE
            
            cell = state.board.get_cell(piece.position)
            if cell and cell.is_safe:
                score += SAFETY_BONUS
                
            threat_penalty = self._calculate_threats(state, piece)
            score -= threat_penalty
            
        return score

    def _calculate_threats(self, state: State, piece: any) -> float:
        THREAT_WEIGHT = 3.0
        threat_score = 0.0
        
        if piece.is_home or piece.is_done:
            return 0.0
            
        for player in state.players:
            if player != state.current_player:
                for opp_piece in player.pieces:
                    if not opp_piece.is_home and not opp_piece.is_done:
                        distance = abs(piece.position - opp_piece.position)
                        if distance <= 6:
                            threat_score += (6 - distance) * THREAT_WEIGHT
        
        return threat_score

  