# tests/fixtures/p05_advanced_code.py
"""Advanced code for scope testing."""

def top_level_func():
    print("global scope")

class MyAdvancedClass:
    """A class with methods."""
    
    class_variable = 1

    def method_a(self):
        """A method."""
        local_to_a = 1
        print("in method_a")

    def method_b(self):
        """Another method."""
        # Этот цикл мы будем искать
        while True:
            break