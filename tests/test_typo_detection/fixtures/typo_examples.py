"""Test fixtures with intentional typos for testing typo detection."""

# Example 1: Simple class with attribute typos
class Hero:
    def __init__(self):
        self.scale = 1.0
        self.sped = 300  # Should be 'speed'
        self.helth = 100  # Should be 'health'
        self.center_x = 50
        self.centre_y = 50  # Should be 'center_y'


# Example 2: Function with typos
def proces_data():  # Should be 'process_data'
    """Process some data."""
    pass


def initalize():  # Should be 'initialize'
    """Initialize something.""" 
    pass


# Example 3: Class with method typos
class GameEngine:
    def updat(self):  # Should be 'update'
        """Update game state."""
        pass
    
    def rendr(self):  # Should be 'render'
        """Render the game."""
        pass


# Example 4: Global variables with typos
SCREAN_WIDTH = 800  # Should be 'SCREEN_WIDTH'
SCREAN_HEIGHT = 600  # Should be 'SCREEN_HEIGHT'
GAME_TITEL = "My Game"  # Should be 'GAME_TITLE'


# Example 5: Complex nested structure
class Player:
    def __init__(self):
        self.positon_x = 0  # Should be 'position_x'
        self.positon_y = 0  # Should be 'position_y'
        self.velocty = 0    # Should be 'velocity'
        
    def move_forwrd(self):  # Should be 'move_forward'
        """Move player forward."""
        pass