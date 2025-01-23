import random

class Dice:
    def __init__(self):
        self.current_value = None
        self._calculate_probabilities()
        
    def _calculate_probabilities(self):
        self.probabilities = {}
        for value in range(1, 6):
            self.probabilities[(value,)] = 1/6
        self.probabilities[(6,)] = 1/6
        for second in range(1, 6):
            self.probabilities[(6, second)] = 1/36
        self.probabilities[(6, 6)] = 1/36
        for third in range(1, 7):
            self.probabilities[(6, 6, third)] = 1/216
    
    def get_probabilities(self, current_sequence=None):
        if not current_sequence:
            return {i: 1/6 for i in range(1, 7)}
            
        if len(current_sequence) == 1:
            if current_sequence[0] == 6:
                return {i: 1/6 for i in range(1, 7)}
            else:
                return {}
                
        if len(current_sequence) == 2:
            if all(x == 6 for x in current_sequence):
                return {i: 1/6 for i in range(1, 7)}
            else:
                return {}
        return {}
    
    def roll(self):
        self.current_value = random.randint(1, 6)
        return self.current_value 