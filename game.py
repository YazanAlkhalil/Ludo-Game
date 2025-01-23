from board import Board
from dice import Dice
from expectiminimax import Expectiminimax, Move
from player import Player
from state import State, StateManager
import copy


class Game:
    def __init__(self, player_colors, is_computer):
        self.board = Board(player_colors[0], player_colors[1], is_computer)
        self.state_manager = StateManager()
        self.dice = Dice()
        self.expectiminimax = Expectiminimax(depth=4, player=self.board.current_player)
    
    def switch_player(self):
        self.board.switch_player()
    
    def computer_move(self, player: Player, dice_value: int):
        current_player = player
        previous_state = self.state_manager.get_last_state()
        current_state = State(
            board=self.board,
            player=current_player,
            parent=previous_state,
            dice_value=dice_value
        )
        self.state_manager.save_state(current_state)
        valid_moves = self.board.get_valid_moves(current_player, dice_value)
        
        if not valid_moves:
            print("Computer has no valid moves available.")
            return
        
        best_move = self.expectiminimax.find_best_move(current_state)
        
        if best_move is None:
            print("Using first valid move as fallback")
            chosen_move = valid_moves[0]
        else:
            chosen_move = None
            for piece, steps in valid_moves:
                if piece.number == best_move.piece.number and steps == dice_value:
                    chosen_move = (piece, steps)
                    break
            
            if not chosen_move:
                print("Best move not found in valid moves, using first valid move")
                chosen_move = valid_moves[0]
        
        piece, steps = chosen_move
        print(f"Computer moves piece {piece.number} by {steps} steps")
        _ = self.board.move_piece(piece, steps)
        dice_history = current_state.get_last_n_dice_values(3)
        consecutive_sixes = sum(1 for x in dice_history if x == 6)
        
        if dice_value == 6 and consecutive_sixes < 3:
            print("Computer gets another roll!")
            new_roll = self.dice.roll()
            print(f"Computer rolled: {new_roll}")
            self.computer_move(current_player, new_roll)
        elif consecutive_sixes >= 3:
            print("Three consecutive sixes! Turn ends.")
            self.board.switch_player()
    
    def player_move(self, player: Player, dice_value: int):
        valid_moves = self.board.get_valid_moves(player, dice_value)
        if not valid_moves:
            print("No valid moves available.")
            return
        
        for idx, (piece, steps) in enumerate(valid_moves):
            print(f"{idx}: Move piece {piece.number +1} by {steps} steps")
        
        while True:
            try:
                choice = int(input("Select move: "))
                if 0 <= choice < len(valid_moves):
                    piece, steps = valid_moves[choice]
                    captured = self.board.move_piece(piece, steps)
                    state = State(
                        board= self.board,
                        player=self.board.current_player,
                        dice_value=dice_value
                    )
                    self.state_manager.save_state(state)

                    return captured
                    break
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")