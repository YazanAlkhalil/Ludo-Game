from game import Game
from color import Color

def test_game_play():
    game = Game()
    game.board.print_board()
    
    # Simulate a series of moves
    for _ in range(10):
        if game.play_turn():
            break

if __name__ == "__main__":
    test_game_play() 