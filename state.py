import copy

class State:
    def __init__(self, board, player, parent=None, dice_value=None):
        self.board = copy.deepcopy(board)
        self.current_player = copy.deepcopy(player)
        self.players = [
            copy.deepcopy(self.board.player1),
            copy.deepcopy(self.board.player2)
        ]
        self.dice_value = dice_value
        self.parent = parent  
        self.opponent = self.board.player2 if player == self.board.player1 else self.board.player1
        self._sync_pieces_with_board()
    
    def _sync_pieces_with_board(self):
        for cell in self.board.cells:
            cell.pieces = []
        for player in self.players:
            for piece in player.pieces:
                if piece.position != -1:
                    cell = self.board.get_cell(piece.position)
                    if cell:
                        cell.pieces.append(piece)
    
    def apply_dice_roll(self, value: int) -> 'State':
        new_state = copy.deepcopy(self)
        new_state.parent = self
        new_state.dice_value = value
        return new_state
    
    def apply_move(self, move) -> 'State':
        new_state = copy.deepcopy(self)
        new_state.parent = self
        captured = False
        
        piece = self._find_piece_in_new_state(new_state, move.piece)
        if piece:
            if piece.position != -1:
                old_cell = new_state.board.get_cell(piece.position)
                if old_cell:
                    old_cell.pieces = [p for p in old_cell.pieces 
                                     if p.number != piece.number or p.color != piece.color]
            
            next_pos = new_state.board.get_next_position(piece.position, move.steps, piece.color)
            if next_pos != -1:
                new_cell = new_state.board.get_cell(next_pos)
                if new_cell:
                    if new_cell.pieces and new_cell.pieces[0].color != piece.color and not new_cell.is_safe:
                        captured = True
                        captured_piece = new_cell.pieces[0]
                        captured_piece.position = -1
                        captured_piece.is_home = True
                        new_cell.pieces.clear()
                    
                    new_cell.pieces.append(piece)
                    piece.position = next_pos
                    piece.is_home = False
                    
                    path = new_state.board.paths[piece.color]
                    if next_pos == path['home_start'] + 5:
                        piece.is_done = True
            
        if not captured and not self._should_keep_turn():
            new_state.switch_player()

        new_state.dice_value = None
        return new_state
    
    def get_valid_moves(self) -> list:
        return self.board.get_valid_moves(self.current_player, self.dice_value)
    
    def evaluate(self) -> float:
        score = 0.0
        opponent = self.opponent
        
        PIECE_VALUE = 25.0           
        PROGRESS_WEIGHT = 0.8        
        SAFE_SPOT_BONUS = 15.0       
        WINNING_BONUS = 500.0        
        HOME_PENALTY = -10.0         
        CAPTURE_OPPORTUNITY = 20.0   
        NEAR_HOME_BONUS = 35.0       
        RISK_PENALTY = -12.0         
        
        if self.current_player.is_winning():
            return WINNING_BONUS
        elif opponent.is_winning():
            return -WINNING_BONUS
        
        for piece in self.current_player.pieces:
            if piece.is_done:
                score += PIECE_VALUE * 2
                score += (WINNING_BONUS * 0.2)  
                continue
                
            if piece.is_home:
                score += HOME_PENALTY
                continue
                
            path = self.board.paths[piece.color]
            if piece.position >= path["home_start"]:
                home_progress = (piece.position - path["home_start"]) / 5.0
                score += NEAR_HOME_BONUS + (home_progress * PIECE_VALUE)
            else:
                total_distance = (path["end"] - path["start"]) % 52
                current_distance = (piece.position - path["start"]) % 52
                progress = current_distance / total_distance
                score += progress * PIECE_VALUE * PROGRESS_WEIGHT
            
            cell = self.board.get_cell(piece.position)
            if cell:
                if cell.is_safe:
                    score += SAFE_SPOT_BONUS
                else:
                    threats = 0
                    for opp_piece in opponent.pieces:
                        if not opp_piece.is_home and not opp_piece.is_done:
                            distance = (opp_piece.position - piece.position) % 52
                            if 1 <= distance <= 6:
                                threats += 1
                                risk = (7 - distance) * RISK_PENALTY / max(threats, 2)
                                score += risk
                                
                                if distance <= 3:
                                    score += CAPTURE_OPPORTUNITY / 2
        
        opponent_weight = 0.7 
        for piece in opponent.pieces:
            if piece.is_done:
                score -= PIECE_VALUE * opponent_weight
            elif not piece.is_home:
                for my_piece in self.current_player.pieces:
                    if not my_piece.is_home and not my_piece.is_done:
                        distance = (piece.position - my_piece.position) % 52
                        if 1 <= distance <= 6:
                            score += CAPTURE_OPPORTUNITY * (7 - distance) / 6
        
        return score

    def is_terminal(self) -> bool:
        return (self.current_player.is_winning() or 
                (self.board.player1.is_winning() or self.board.player2.is_winning()))
    
    def _find_piece_in_new_state(self, new_state, original_piece):
        
        for piece in new_state.current_player.pieces:
            if piece.number == original_piece.number:
                return piece
        return None

    def _should_keep_turn(self) -> bool:
        if self.dice_value != 6:
            return False

        consecutive_sixes = 1
        current = self
        while current.parent and consecutive_sixes < 3:
            if current.parent.dice_value == 6:
                consecutive_sixes += 1
            else:
                break
            current = current.parent

        return consecutive_sixes < 3

    def get_last_n_dice_values(self, n: int) -> list:
        values = []
        current = self
        current_sequence = []
        
        while current and len(current_sequence) < n:
            if current.dice_value is not None:
                if not current_sequence or current.dice_value == 6:
                    current_sequence.append(current.dice_value)
            current = current.parent
            
            if current and current.dice_value is not None and current.dice_value != 6:
                break
        
        return current_sequence

    def switch_player(self):
        self.current_player = (
            self._find_player_in_state(self.board.player2) 
            if self.current_player.color == self.board.player1.color 
            else self._find_player_in_state(self.board.player1)
        )

    def _find_player_in_state(self, original_player):
        for player in self.players:
            if player.color == original_player.color:
                return player
        return None

class StateManager:
    def __init__(self):
        self.states = []
    
    def save_state(self, state: State):
        self.states.append(state)
    
    def get_last_state(self) -> State:
        return self.states[-1] if self.states else None
    
    def clear_history(self):
        self.states.clear()