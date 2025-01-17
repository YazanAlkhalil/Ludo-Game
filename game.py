from board import Board
from dice import Dice
from expectiminimax import Expectiminimax, Move
from player import Player
from state import State, StateManager


class Game:
    def __init__(self, player_colors, is_computer):
        self.board = Board(player_colors[0], player_colors[1], is_computer)
        self.state_manager = StateManager()
        self.dice = Dice()
        self.expectiminimax = Expectiminimax(depth=3)
    
    def switch_player(self):
        self.board.switch_player()
    
    def computer_move(self):
        current_state = self.state_manager.get_last_state()
        if not current_state:
            # إنشاء حالة أولية إذا لم تكن موجودة
            current_state = State(
                board=self.board,
                player=self.board.current_player,
                action=None,
                cost=0,
                depth=0,
                parent=None
            )
            self.state_manager.save_state(self.board, self.board.current_player, None, cost=0)
        
        best_move = self.expectiminimax.find_best_move(current_state)
        if best_move:
            print(f"Computer moves piece {best_move.piece.number} by {best_move.steps} steps")
            self.board.move_piece(best_move.piece, best_move.steps)
            self.state_manager.save_state(self.board, self.board.current_player, best_move, cost=0)
        else:
            print("Computer has no valid moves")
    def player_move(self, player: Player, dice_value: int):
        valid_moves = self.board.get_valid_moves(player, dice_value)
        if not valid_moves:
            print("No valid moves available.")
            return
        
        # Display valid moves
        for idx, (piece, steps) in enumerate(valid_moves):
            print(f"{idx}: Move piece {piece.number} by {steps} steps")
        
        while True:
            try:
                choice = int(input("Select move: "))
                if 0 <= choice < len(valid_moves):
                    piece, steps = valid_moves[choice]
                    self.board.move_piece(piece, steps)
                    
                    move = Move(piece=piece, steps=steps)
                    self.state_manager.save_state(self.board, self.board.current_player, move, cost=0)
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")