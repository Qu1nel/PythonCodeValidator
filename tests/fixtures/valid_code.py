"""A valid sample file for testing."""

import sys

GLOBAL_CONSTANT = "HELLO"

class MyParent:
    pass

class MyTestClass(MyParent):
    """A test class."""
    def __init__(self):
        self.value = 10

    def solve(self, a, b):
        """A test method."""
        local_var = a + b
        return local_var

def main():
    """Main entry point."""
    print("OK")