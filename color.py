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
        """Get single-character symbol for the color"""
        return {
            "blue": "B",    # يمكنك استخدام أحرف بدلاً من الرموز التعبيرية
            "red": "R",
            "green": "G",
            "yellow": "Y",
            "white": "W"
        }.get(self.value, "W")