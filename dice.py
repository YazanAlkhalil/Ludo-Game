import random

class Dice:
    def __init__(self):
        self.current_value = None
        
    def roll(self):
        """
        Roll the dice according to game rules:
        - Rolling 6 gives an extra turn
        - Player gets additional roll after moving piece
        """
        self.current_value = random.randint(1, 6)
        return self.current_value
    
    def get_probabilities(self):
        """Get probability distribution for dice rolls"""
        # Equal probability (1/6) for each value
        return {i: 1/6 for i in range(1, 7)} 