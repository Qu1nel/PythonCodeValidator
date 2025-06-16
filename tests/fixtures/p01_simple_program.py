"""Simple program for basic checks."""
# Этот файл должен проходить базовую валидацию
import sys

GLOBAL_CONST = "ALLOWED"


def solve():
    """This function is required."""
    x = 12  # local var
    print(x)
    print(sys.version)


def main():
    """Main function calls solve."""
    solve()


if __name__ == "__main__":
    main()
