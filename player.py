from path import Path
from piece import Piece
from color import Color

class Player:
    def __init__(self, color: Color, path: Path, is_computer: bool = False):
        self.color = color
        self.pieces = [Piece(color, i) for i in range(4)]  # Only 2 pieces per player
        self.path = path
        self.is_computer = is_computer
        
    def has_valid_moves(self, dice_value, board):
        """Check if player has any valid moves with given dice value"""
        return any(piece.can_move(dice_value, board) for piece in self.pieces)
    
    def is_winning(self):
        """Player wins when all pieces reach end zone"""
        return all(piece.is_done for piece in self.pieces)