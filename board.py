from cell import Cell
from color import Color
from player import Player

class Board:
    def __init__(self, player_color: Color, computer_color: Color, is_computer_list):
        self.cells = [Cell(Color.WHITE) for _ in range(76)]
        for i in range(52, 58):
            self.cells[i].color = Color.BLUE
        for i in range(58, 64):
            self.cells[i].color = Color.RED
        for i in range(64, 70):
            self.cells[i].color = Color.GREEN
        for i in range(70, 76):
            self.cells[i].color = Color.YELLOW
        
        self.paths = {
            Color.BLUE: {"start": 0, "end": 50, "home_start": 52},
            Color.RED: {"start": 13, "end": 11, "home_start": 58},
            Color.GREEN: {"start": 26, "end": 24, "home_start": 64},
            Color.YELLOW: {"start": 39, "end": 37, "home_start": 70}
        }
        
        '''
        #TODO 
        why to add them
        '''
        
        
        # إنشاء اللاعبين
        self.player1 = Player(player_color, is_computer_list[0])
        self.player2 = Player(computer_color, is_computer_list[1])
        
        # تحديد اللاعب الحالي
        self.current_player = self.player1
        
        self._initialize_board()
    
    def _initialize_board(self):
        """تهيئة اللوحة مع الخلايا الآمنة ونقاط البداية"""
        # تعيين نقاط البداية كخلايا آمنة
        for color, path in self.paths.items():
            start_pos = path["start"]
            self.cells[start_pos].color = color
            self.cells[start_pos].is_safe = True
    
    def get_cell(self, position: int) -> Cell:
        """Get the cell at the specified position"""
        if 0 <= position < 76:  # Updated from 72 to 76
            return self.cells[position]
        return None

    def get_next_position(self, current_pos: int, steps: int, color: Color) -> int:
        """Calculate next position considering home path"""
        path = self.paths[color]
        
        # If piece is in home base
        if current_pos == -1:
            if steps == 6:  # Can only move out with a 6
                return path["start"]
            return -1
        
        # Calculate next position on main board
        new_pos = current_pos + steps
        
        # If piece is already in home path
        if current_pos >= path["home_start"]:
            # Check if move stays within the color's home path range
            home_end = path["home_start"] + 5
            if new_pos <= home_end:
                return new_pos
            return -1
        
        # Check if piece should enter home path
        if new_pos > path["end"] and current_pos <= path["end"]:
            overflow = new_pos - path["end"] - 1
            home_pos = path["home_start"] + overflow
            if home_pos <= path["home_start"] + 5:
                return home_pos
            return -1
        
        # Normal movement on main board
        if new_pos > 51:
            new_pos = new_pos - 52

        return new_pos

    def print_board(self):
        """Enhanced board printing with home paths"""
        COLORS = {
            Color.BLUE: '\033[94m',    # Blue
            Color.RED: '\033[91m',     # Red
            Color.GREEN: '\033[92m',   # Green
            Color.YELLOW: '\033[93m',  # Yellow
            Color.WHITE: '\033[97m',   # White
            'RESET': '\033[0m'         # Reset
        }
        
        def format_home_cell(path, index):
            """Format home path cell"""
            if 52 <= index <= 57:
                cell = path.cells[index]
                if cell.pieces:
                    piece = cell.pieces[0]
                    return f"{COLORS[piece.color]}{piece.color.symbol}{COLORS['RESET']}"
                return "·"
            return " "
        
        # Corrected board template with proper cross pattern
        # Corrected board template with proper cross pattern
        board_template = [
            "                            ┌───┬───┬───┐       ",
            "                            │ {c49} │ {c50} │ {c51} │       ",
            "                            ├───┼───┼───┤       ",
            "                            │ {c48} │ {c52} │ {c0} │       ",
            "                            ├───┼───┼───┤         ",
            "                            │ {c47} │ {c53} │ {c1} │         ",
            "         {YELLOW}YELLOW{RESET}             ├───┼───┼───┤              {BLUE}BLUE{RESET}",
            "                            │ {c46} │ {c54} │ {c2} │         ",
            "                            ├───┼───┼───┤         ",
            "                            │ {c45} │ {c55} │ {c3} │         ",
            "                            ├───┼───┼───┤         ",
            "                            │ {c44} │ {c56} │ {c4} │         ",
            "    ┌───┬───┬───┬───┬───┬───┼───┼───┼───┼───┬───┬───┬───┬───┐───┐    ",
            "    │ {c38} │ {c39} │ {c40} │ {c41} │ {c42} │ {c43} │   │ {c57} │   │ {c5} │ {c6} │ {c7} │ {c8} │ {c9} │ {c10} |    ",
            "    ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤    ",
            "    │ {c37} │ {c70} │ {c71} │ {c72} │ {c73} │ {c74} │ {c75} │   │ {c63} │ {c62} │ {c61} │ {c60} │ {c59} │ {c58} │ {c11} |    ",
            "    ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤    ",
            "    │ {c36} │ {c35} │ {c34} │ {c33} │ {c32} │ {c31} │   │ {c69} │   │ {c17} │ {c16} │ {c15} │ {c14} │ {c13} │ {c12} |    ",
            "    └───┴───┴───┴───┴───┴───┼───┼───┼───┼───┴───┴───┴───┴───┴───┘    ",
            "                            │ {c30} │ {c68} │ {c18} │           ",
            "                            ├───┼───┼───┤           ",
            "                            │ {c29} │ {c67} │ {c19} │           ",
            "                            ├───┼───┼───┤           ",
            "                            │ {c28} │ {c66} │ {c20} │           ",
            "         {GREEN}GREEN{RESET}              ├───┼───┼───┤                 {RED}RED{RESET}   ",
            "                            │ {c27} │ {c65} │ {c21} │            ",
            "                            ├───┼───┼───┤           ",
            "                            │ {c26} │ {c64} │ {c22} │           ",
            "                            ├───┼───┼───┤           ",
            "                            │ {c25} │ {c24} │ {c23} │           ",
            "                            └───┴───┴───┘              "
        ]


        def format_cell(cell_idx):
            """Format the cell with appropriate color and symbol"""
            cell = self.get_cell(cell_idx)
            if not cell:
                return " "
            
            if cell_idx in [57, 63, 69, 75]:
                piece_count = len(cell.pieces) if cell.pieces else 0
                if piece_count > 0:
                    return f"{COLORS[cell.color]}{piece_count}{COLORS['RESET']}"
                return f"{COLORS[cell.color]}0{COLORS['RESET']}"
            
            # Display piece number if present
            if cell.pieces:
                piece = cell.pieces[0]
                return f"{COLORS[piece.color]}{piece.number + 1}{COLORS['RESET']}"
            
            # Display safe cell symbol if no piece is present
            if cell.is_safe and cell_idx < 52:
                return f"{COLORS[cell.color]}★{COLORS['RESET']}"
            
            if cell_idx >= 52:
                return f"{COLORS[cell.color]}○{COLORS['RESET']}"
            
            return "·"

        cell_dict = {
            'GREEN': COLORS[Color.GREEN],
            'RED': COLORS[Color.RED],
            'YELLOW': COLORS[Color.YELLOW],
            'BLUE': COLORS[Color.BLUE],
            'RESET': COLORS['RESET']
        }
        
        for i in range(76):
            cell_dict[f'c{i}'] = format_cell(i)
        
        print("\n=== LUDO GAME ===\n")
        for line in board_template:
            print(line.format(**cell_dict))
        
        
        print("\nPieces in home:")
        for player in [self.player1, self.player2]:
            home_pieces = [p for p in player.pieces if p.is_home]
            if home_pieces:
                print(f"{COLORS[player.color]}{player.color.value}: " + 
                      ", ".join([f"P{p.number}" for p in home_pieces]) + 
                      f"{COLORS['RESET']}")

    def switch_player(self):
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def move_piece(self, piece, steps):
        print(f"piece position {piece.position}")
        next_pos = self.get_next_position(piece.position, steps, piece.color)
        path = self.paths[piece.color]
        
        if not piece.can_move(steps, self):
            print('piece cantmove')
            return False
        # Check if move is valid
        old_pos = piece.position
        new_cell = self.get_cell(next_pos)


        
        if not new_cell:
            print('not cell')
            return False
        
        captured_opponent = False
        # Check if we're capturing an opponent's piece
        if new_cell.pieces and new_cell.pieces[0].color != piece.color and not new_cell.is_safe:
            captured_piece = new_cell.pieces[0]
            captured_piece.position = -1  # Send back to home
            captured_piece.is_home = True
            new_cell.pieces.clear()
            captured_opponent = True
        
        # Remove piece from old position
        if old_pos != -1:
            old_cell = self.get_cell(old_pos)
            if old_cell:
                old_cell.pieces.remove(piece)
        
        # Add piece to new position
        new_cell.pieces.append(piece)
        piece.position = next_pos
        piece.is_home = False

        # piece reached end
        if next_pos == path['home_start'] + 5:
            piece.is_done = True
        
        return  captured_opponent

    def get_valid_moves(self, player, dice_value) -> list:
        """Get all valid moves for the current player"""
        valid_moves = []
        
        # Check each piece for valid moves
        for piece in player.pieces:
            if piece.can_move(dice_value, self):
                valid_moves.append((piece, dice_value))
        
        return valid_moves
