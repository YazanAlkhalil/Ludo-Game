import copy

class State:
    def __init__(self, board, player, action=None, cost=0, depth=0, parent=None):
        self.board = copy.deepcopy(board)
        self.current_player = copy.deepcopy(player)
        self.action = action
        self.cost = cost
        self.depth = depth
        self.parent = parent
        self.dice_value = None
        
        # Ensure pieces in cells reference the copied pieces
        for piece in self.current_player.pieces:
            if piece.position != -1:
                cell = self.board.get_cell(piece.position)
                if cell:
                    cell.pieces = [p for p in cell.pieces if p.color != piece.color]
                    cell.pieces.append(piece)

class StateManager:
    def __init__(self):
        self.states = []
        
    def create_state(self, board, player, action, cost=0):
        """Create a new state from the given information"""
        depth = len(self.states)
        parent = self.states[-1] if self.states else None
        
        new_state = State(
            board=board,
            player=player,
            action=action,
            cost=cost,
            depth=depth,
            parent=parent
        )
        return new_state
    
    def save_state(self, board, player, action, cost=0):
        """Create and save a new state"""
        new_state = self.create_state(board, player, action, cost)
        self.states.append(new_state)
        return new_state
    
    def get_last_state(self):
        """Get the most recent state"""
        return self.states[-1] if self.states else None
    
    def clear_states(self):
        """Clear all saved states"""
        self.states = []