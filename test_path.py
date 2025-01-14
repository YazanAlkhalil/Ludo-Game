from color import Color
from path import Path

def test_paths():
    # إنشاء وطباعة مسار لكل لون
    colors = [Color.BLUE, Color.RED, Color.GREEN, Color.YELLOW]
    
    for color in colors:
        path = Path(color)
        path.print_path()
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    test_paths()