
"""
Applied Cryptograpy II  :   Homework 3 Battleship game.
Student                 :   Sowat Kheang
Howework 3              :   Implementing a full Battleship board 10x10 matrix and each player 
                            has 5 boats with sizes of 5, 4, 3, 2 and 2 dots using homomorphic encryption 
                            to hide the board information
                        
Run the program         :   python3 homework_3_battleship_game.py
"""

import random
from math import gcd
from enum import Enum

# Battleship Game Logic
BOARD_SIZE = 10                      # 10x10 board
BOAT_SIZES = [5, 4, 3, 2, 2]         # Boat sizes: 5, 4, 3, 2, 2 (total 16 cells)

class Choice(Enum):
    HORIZONTAL = 1
    VERTICAL = 2


# Create an empty board
def create_board():
    """
        Create an empty battleship board.
        0 represents an empty cell
        1 represents a boat part
    """
    return [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# Place boats on the board
def place_boats(board):
    """
        Place boats randomly on the board.
        Boats can be placed either horizontally or vertically.
        - Boats do not overlap with each other.
        - Boats stay within the board boundaries.
    """
    for boat_size in BOAT_SIZES:
        placed = False
        
        while not placed:
            
            orientation = random.choice([Choice.HORIZONTAL, Choice.VERTICAL])  # Horizontal or Vertical
            
            match orientation:
                case Choice.HORIZONTAL:
                    row = random.randint(0, BOARD_SIZE - 1)
                    col = random.randint(0, BOARD_SIZE - boat_size)
                    if all(board[row][col + i] == 0 for i in range(boat_size)):
                        for i in range(boat_size):
                            board[row][col + i] = 1
                        placed = True
                case Choice.VERTICAL:
                    row = random.randint(0, BOARD_SIZE - boat_size)
                    col = random.randint(0, BOARD_SIZE - 1)
                    if all(board[row + i][col] == 0 for i in range(boat_size)):
                        for i in range(boat_size):
                            board[row + i][col] = 1
                        placed = True
                        
    # ? Haven't tested yet
    print(board)


# Main function
def main():
    print(f"\nWelcome to the Battleship Game with Homomorphic Encryption\n")
    
    # Test create board
    board = create_board()
    place_boats(board)
    
    # Create boards for two players
    # TODO:

if __name__ == "__main__":
    random.seed(42)
    main()