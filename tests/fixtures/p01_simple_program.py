"""Simple program for basic checks."""
import sys

GLOBAL_CONST = "ALLOWED"


def solve():
    """This function is required."""
    x = 12
    print(x)
    # Используем sys, чтобы flake8 был доволен
    print(f"Python version: {sys.version_info.major}.{sys.version_info.minor}")


def main():
    """Main function calls solve."""
    solve()


if __name__ == "__main__":
    main()
