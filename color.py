from enum import Enum

class Color(Enum):
    BLUE = "blue"
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    WHITE = "white"
    
    def __str__(self):
        return self.value
    
    @property
    def symbol(self):
        return {
            "blue": "B",    
            "red": "R",
            "green": "G",
            "yellow": "Y",
            "white": "W"
        }.get(self.value, "W")