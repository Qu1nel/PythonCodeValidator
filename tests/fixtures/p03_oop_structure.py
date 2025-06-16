"""Program for testing OOP validation rules."""

class Parent:
    pass

class CorrectChild(Parent):
    """Correctly inherits and has required attributes."""
    def __init__(self, name):
        self.name = name
        self.value: int = 0

class WrongChild:
    """Incorrectly defined class."""
    def __init__(self):
        self.name = "default"