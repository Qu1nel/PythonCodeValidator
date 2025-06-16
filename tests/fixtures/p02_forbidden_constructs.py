"""Program with forbidden constructs."""
import os # Запрещенный импорт
from sys import exit # Запрещенный импорт из

GLOBAL_VAR = 123 # Не константа

def main():
    """This function uses forbidden calls."""
    eval("1+1") # Запрещенный вызов
    while True: # Запрещенный цикл
        break