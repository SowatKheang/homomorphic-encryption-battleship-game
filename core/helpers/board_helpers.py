
import random
from enum import Enum
from core.constants.const import BOARD_SIZE, BOAT_SIZES, RED, BLUE, YELLOW, RESET

class BoardOrientation(Enum):
    HORIZONTAL = 1
    VERTICAL = 2
    
# 
# Create an empty board
# 
def create_board():
    """
        Create an empty battleship board.
        0 represents an empty cell
        1 represents a boat part
    """
    return [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# 
# Place boats on the board
#
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
            
            orientation = random.choice([BoardOrientation.HORIZONTAL, BoardOrientation.VERTICAL])
            
            match orientation:
                case BoardOrientation.HORIZONTAL:
                    row = random.randint(0, BOARD_SIZE - 1)
                    col = random.randint(0, BOARD_SIZE - boat_size)
                    if all(board[row][col + i] == 0 for i in range(boat_size)):
                        for i in range(boat_size):
                            board[row][col + i] = 1
                        placed = True
                case BoardOrientation.VERTICAL:
                    row = random.randint(0, BOARD_SIZE - boat_size)
                    col = random.randint(0, BOARD_SIZE - 1)
                    if all(board[row + i][col] == 0 for i in range(boat_size)):
                        for i in range(boat_size):
                            board[row + i][col] = 1
                        placed = True
                        
# 
# Encrypt the board with Paillier public key
#
def encrypt_board(plain_board, public_key):
    """
        Encrypt all cells in the  board with the given Paillier public key.
        The result is a BOARD_SIZE x BOARD_SIZE matrix of ciphertexts.
    """
    encrypted_board = []

    for row_index in range(BOARD_SIZE):
        encrypted_row = []
        for col_index in range(BOARD_SIZE):
            cell_value = plain_board[row_index][col_index]  # 0 empty or 1 boat part
            encrypted_cell = public_key.encrypt(cell_value)
            encrypted_row.append(encrypted_cell)
        encrypted_board.append(encrypted_row)

    return encrypted_board

# 
# Print player board helper function
#
def print_player_board(player_board, player_name):
    print(f"{YELLOW}<<== [DEBUG] {player_name}'s plain board (1 = boat, 0 = empty):{RESET}")
    for row in player_board:
        # if item in row is 1, print blue else print white
        print("   ", end="")
        for item in row:
            if item == 1:
                print(f"{BLUE}1{RESET}", end=" ") # This code prints in blue color
            else:
                print("0", end=" ")
        print()
    print()