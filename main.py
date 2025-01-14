from game import Game
from color import Color

def setup_game():
    # Get number of players
    while True:
        try:
            num_players = int(input("Enter number of players (2-4): "))
            if 2 <= num_players <= 4:
                break
            print("Please enter a number between 2 and 4")
        except ValueError:
            print("Please enter a valid number")

    # Available colors
    available_colors = [Color.BLUE, Color.RED, Color.GREEN, Color.YELLOW]
    players = []

    # Get color for each player
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
    # Get player setup
    players = setup_game()
    
    # تقسيم players إلى قائمتين
    player_colors = [p[0] for p in players]
    is_computer = [p[1] for p in players]
    
    # إنشاء اللعبة مع المعاملات الصحيحة
    game = Game(player_colors, is_computer)
    game.board.print_board()
    consecutive_rolls = 0   
    
    while True:
        current_player = game.board.current_player
        dice_value = game.dice.roll()
        print(f"\nPlayer {current_player.color.value} rolled a {dice_value}")
        
        if current_player.is_computer:
            game.computer_move()
        else:
            valid_moves = game.board.get_valid_moves(current_player, dice_value)
            if valid_moves:
                game.player_move(current_player, dice_value)
            else:
                print("No valid moves available")
        
        game.board.print_board()
        
        if current_player.is_winning():
            print(f"\nPlayer {current_player.color.value} wins!")
            break
        
        if dice_value == 6:
            consecutive_rolls += 1
            if consecutive_rolls >= 3:
                print("Maximum consecutive rolls reached.")
                game.board.switch_player()
                consecutive_rolls = 0
        else:
            game.board.switch_player()
            consecutive_rolls = 0

if __name__ == "__main__":
    main()