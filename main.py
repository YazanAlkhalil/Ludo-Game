from game import Game
from color import Color

def setup_game():
    while True:
        try:
            num_players = int(input("Enter number of players (2-4): "))
            if 2 <= num_players <= 4:
                break
            print("Please enter a number between 2 and 4")
        except ValueError:
            print("Please enter a valid number")

    available_colors = [Color.BLUE, Color.RED, Color.GREEN, Color.YELLOW]
    players = []

    for i in range(num_players):
        print(f"\nAvailable colors for Player {i+1}:")
        for idx, color in enumerate(available_colors):
            print(f"{idx + 1}: {color.value}")
        
        while True:
            try:
                choice = int(input(f"Choose color for Player {i+1}: ")) - 1
                if 0 <= choice < len(available_colors):
                    color = available_colors.pop(choice)
                    is_computer = input(f"Is Player {i+1} a computer? (y/n): ").lower() == 'y'
                    players.append((color, is_computer))
                    break
                print("Invalid choice")
            except ValueError:
                print("Please enter a valid number")

    return players

def main():
     
    players = setup_game()
    player_colors = [p[0] for p in players]
    is_computer = [p[1] for p in players]
    game = Game(player_colors, is_computer)
    game.board.print_board()
    COLORS = {
        Color.BLUE: '\033[94m',   
        Color.RED: '\033[91m',    
        Color.GREEN: '\033[92m',  
        Color.YELLOW: '\033[93m', 
        Color.WHITE: '\033[97m',  
        'RESET': '\033[0m'        
    }
    
    while True:
        current_player = game.board.current_player
        consecutive_sixes = 0  
        keep_rolling = True
        
        while keep_rolling:
            dice_value = game.dice.roll()
            print(f"\nPlayer {COLORS[current_player.color]}{current_player.color.value}{COLORS['RESET']} rolled a {dice_value}")
            
            if dice_value == 6:
                consecutive_sixes += 1
                if consecutive_sixes >= 3:
                    print("Three consecutive 6s! Turn forfeited.")
                    keep_rolling = False
                    game.board.switch_player()
                    break
            else:
                keep_rolling = False  
            
            valid_moves = game.board.get_valid_moves(current_player, dice_value)
            if valid_moves:
                if current_player.is_computer:
                    game.computer_move(current_player, dice_value)
                else:
                    game.player_move(current_player, dice_value)
            else:
                print("No valid moves available")
            
            game.board.print_board()
            
            if current_player.is_winning():
                print(f"\nPlayer {current_player.color.value} wins!")
                return
        
        if dice_value != 6 or consecutive_sixes >= 3:
            game.board.switch_player()

if __name__ == "__main__":
    main()