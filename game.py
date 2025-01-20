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
        self.expectiminimax = Expectiminimax(depth=3)
    
    def switch_player(self):
        self.board.switch_player()
    
    def computer_move(self, player: Player, dice_value: int):
        current_player = player
        
        # Get valid moves
        valid_moves = self.board.get_valid_moves(current_player, dice_value)
        print(f"Valid moves: {valid_moves}")
        
        if not valid_moves:
            print("Computer has no valid moves available.")
            return
        
        # Create a new state for the current board position
        current_state = State(
            board=self.board,
            player=current_player,
            action=None,
            cost=0,
            depth=0,
            parent=None
        )
        current_state.dice_value = dice_value
        
        # Find best move using expectiminimax
        best_move = self.expectiminimax.find_best_move(current_state)
        print(f"Best move: {best_move}")
        
        if best_move is None:
            print("Using first valid move as fallback")
            chosen_move = valid_moves[0]
        else:
            # Match the best move with valid moves
            chosen_move = None
            for piece, steps in valid_moves:
                if piece.number == best_move.piece.number and steps == dice_value:
                    chosen_move = (piece, steps)
                    break
            
            if not chosen_move:
                print("Best move not found in valid moves, using first valid move")
                chosen_move = valid_moves[0]
        
        # Execute the chosen move
        if chosen_move:
            piece, steps = chosen_move
            print(f"Computer moves piece {piece.number + 1} by {steps} steps")
            
            try:
                # Make the move
                self.board.move_piece(piece, steps)
                
                # Save the state
                move = Move(piece=piece, steps=steps)
                self.state_manager.save_state(self.board, current_player, move, cost=0)
                
                # Print updated board
                print("\n=== LUDO GAME ===\n")
                self.board.print_board()
                
                # Print pieces in home
                print("\nPieces in home:")
                for p in [self.board.player1, self.board.player2]:
                    home_pieces = [f"P{piece.number}" for piece in p.pieces if piece.is_home]
                    print(f"{p.color.value}: {', '.join(home_pieces)}")
                
            except Exception as e:
                print(f"Error in computer move: {e}")
    
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