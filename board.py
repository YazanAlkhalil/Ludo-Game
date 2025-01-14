from cell import Cell
from path import Path
from color import Color
from player import Player

class Board:
    def __init__(self, player_color: Color, computer_color: Color, is_computer_list):
        # إنشاء المسار المشترك (52 خلية)
        self.cells = [Cell(Color.WHITE) for _ in range(52)]
        
        # تعيين نقاط البداية والنهاية لكل لون
        self.paths = {
            Color.BLUE: {"start": 0, "end": 51},
            Color.RED: {"start": 13, "end": 12},
            Color.GREEN: {"start": 26, "end": 25},
            Color.YELLOW: {"start": 39, "end": 38}
        }
        
        # إنشاء المسارات
        self.player_path = Path(player_color)
        self.computer_path = Path(computer_color)
        
        # إنشاء اللاعبين
        self.player1 = Player(player_color, self.player_path, is_computer_list[0])
        self.player2 = Player(computer_color, self.computer_path, is_computer_list[1])
        
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
        """الحصول على الخلية في الموقع المحدد"""
        if 0 <= position < 52:
            return self.cells[position]
        return None

    def get_next_position(self, current_pos: int, steps: int, color: Color) -> int:
        """Calculate next position considering home path"""
        path = self.player_path if color == self.player1.color else self.computer_path
        
        # If piece is in home base
        if current_pos == -1:
            if steps == 6:  # Can only move out with a 6
                return path.start_position
            return -1
        
        # Convert global position to local path position
        local_pos = path.get_local_index(current_pos)
        new_local_pos = local_pos + steps
        
        # Check if piece should enter home path
        if path.can_enter_home(current_pos, steps):
            # Get the deepest available spot in home path
            return path.get_deepest_available_home_spot()
        
        # Convert back to global position
        new_global_pos = path.get_global_index(new_local_pos)
        
        # Validate the position
        if new_global_pos < 0 or new_global_pos > 51:
            return -1
        
        return new_global_pos

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
        board_template = [
            "                            ┌───┬───┬───┐       ",
            "                            │ {c49} │ {c50} │ {c51} │       ",
            "                            ├───┼───{BLUE}┼───┤{RESET}       ",
            "                            │ {c48} │ {h1} {BLUE}│ {c0} │{RESET}       ",
            "                            ├───┼───{BLUE}┼───┤{RESET}         ",
            "                            │ {c47} │ {h2} │ {c1} │         ",
            "         {YELLOW}YELLOW{RESET}             ├───┼───┼───┤              {BLUE}BLUE{RESET}",
            "                            │ {c46} │ {h3} │ {c2} │         ",
            "                            ├───┼───┼───┤         ",
            "                            │ {c45} │   │ {c3} │         ",
            "                            ├───┼───┼───┤         ",
            "                            │ {c44} │   │ {c4} │         ",
            "    ┌───┬───┬───┬───┬───┬───┼───┼───┼───┼───┬───┬───┬───┬───┐───┐    ",
            "    │ {c38} │ {c39} │ {c40} │ {c41} │ {c42} │ {c43} │   │   │   │ {c5} │ {c6} │ {c7} │ {c8} │ {c9} │ {c10} |    ",
            "    ├───┼───┼───┼───┼───┼───┼   ┼   ┼   ┼───┼───┼───┼───┼───┼───┤  ",
            "    │ {c37} │   │   │   │   │   │   │   │   │   │   │   │   │   │ {c11} |    ",
            "    ├───┼───┼───┼───┼───┼───┼   ┼   ┼   ┼───┼───┼───┼───┼───┼───┤  ",
            "    │ {c36} │ {c35} │ {c34} │ {c33} │ {c32} │ {c31} │   │   │   │ {c17} │ {c16} │ {c15} │ {c14} │ {c13} │ {c12} |    ",
            "    └───┴───┴───┴───┴───┴───┼───┼───┼───┼───┴───┴───┴───┴───┴───┘    ",
            "                            │ {c30} │   │ {c18} │           ",
            "                            ├───┼───┼───┤           ",
            "                            │ {c29} │   │ {c19} │           ",
            "                            ├───┼───┼───┤           ",
            "                            │ {c28} │   │ {c20} │           ",
            "         {GREEN}GREEN{RESET}              ├───┼───┼───┤                 {RED}RED{RESET}   ",
            "                            │ {c27} │   │ {c21} │            ",
            "                            ├───┼───┼───┤           ",
            "                            │ {c26} │   │ {c22} │           ",
            "                            ├───┼───┼───┤           ",
            "                            │ {c25} │ {c24} │ {c23} │           ",
            "                            └───┴───┴───┘              "
        ]

        def format_cell(cell_idx):
            """Format the cell with appropriate color and symbol"""
            cell = self.get_cell(cell_idx)
            if not cell:
                return " "
            
            if cell.pieces:
                piece = cell.pieces[0]
                return f"{COLORS[piece.color]}{piece.color.symbol}{COLORS['RESET']}"
            
            return "·"

        # Create a dictionary for the template
        cell_dict = {
            'GREEN': COLORS[Color.GREEN],
            'RED': COLORS[Color.RED],
            'YELLOW': COLORS[Color.YELLOW],
            'BLUE': COLORS[Color.BLUE],
            'RESET': COLORS['RESET']
        }
        
        # Add numbered cells to the dictionary
        for i in range(52):
            cell_dict[f'c{i}'] = format_cell(i)
        
        # Add home path cells
        for i in range(1, 7):
            cell_dict[f'h{i}'] = format_home_cell(self.player_path, 51 + i)
        
        # Print the board
        print("\n=== LUDO GAME ===\n")
        for line in board_template:
            print(line.format(**cell_dict))
        
        # Print game status
        print("\nCurrent Player:", 
              f"{COLORS[self.current_player.color]}{self.current_player.color.value}{COLORS['RESET']}")
        
        # Print home pieces
        print("\nPieces in home:")
        for player in [self.player1, self.player2]:
            home_pieces = [p for p in player.pieces if p.is_home]
            if home_pieces:
                print(f"{COLORS[player.color]}{player.color.value}: " + 
                      ", ".join([f"P{p.number}" for p in home_pieces]) + 
                      f"{COLORS['RESET']}")

    def switch_player(self):
        """تبديل اللاعب الحالي"""
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def move_piece(self, piece, steps):
        """تحريك قطعة على اللوحة"""
        next_pos = self.get_next_position(piece.position, steps, piece.color)
        if next_pos == -1:
            return False

        # حفظ الموقع القديم
        old_pos = piece.position
        
        # إزالة القطعة من موقعها القديم
        if old_pos != -1:
            old_cell = self.get_cell(old_pos)
            if old_cell:
                old_cell.pieces.remove(piece)
        
        # إضافة القطعة إلى الموقع الجديد
        new_cell = self.get_cell(next_pos)
        if new_cell and new_cell.can_move_to(piece):
            new_cell.pieces.append(piece)
            piece.position = next_pos
            piece.is_home = False
            return True
            
        return False

    def get_valid_moves(self, player, dice_value):
        """الحصول على جميع التحركات الصالحة للاعب"""
        valid_moves = []
        for piece in player.pieces:
            next_pos = self.get_next_position(piece.position, dice_value, piece.color)
            if next_pos != -1:
                cell = self.get_cell(next_pos)
                if cell and cell.can_move_to(piece):
                    valid_moves.append((piece, dice_value))
        return valid_moves