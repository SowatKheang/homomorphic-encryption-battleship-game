
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
    
# 
# Input validation for guesses
#
def do_valid_guess(player_name, already_guessed_cells):
    """
        Player need to enter a guess "row col", where both are (1 - 10)
        - coordinates are within [1, BOARD_SIZE]
        - the player does not guess the same cell twice
        - returns zero-based indices (0 - 9) for internal use
    """
    while True:
        guess_input = input(
            f"[{player_name}] Enter your guess as 'row col' (1-10 1-10): "
        )

        # Allow formats for example "1 1" or "1,1"
        guess_input = guess_input.replace(",", " ")
        parts = guess_input.split()

        if len(parts) != 2:
            print(f"{RED}<<== Invalid format. Please enter exactly two numbers, e.g. '1 1'.{RESET}")
            continue

        try:
            # For Human coordinates should count from (1–10)
            human_row = int(parts[0])
            human_col = int(parts[1])
        except ValueError:
            print("{RED}<<==Invalid input. Please enter integer numbers, e.g. '1 1'.{RESET}")
            continue

        # Check bounds: 1..BOARD_SIZE in human space
        if not (1 <= human_row <= BOARD_SIZE and 1 <= human_col <= BOARD_SIZE):
            print(f"{RED}<<== Coordinates out of bounds. Use numbers from 1 to {BOARD_SIZE}.{RESET}")
            continue

        # Convert to zero-based indices for machine use
        guessed_row = human_row - 1
        guessed_col = human_col - 1

        # Check if already guessed
        if (guessed_row, guessed_col) in already_guessed_cells:
            print(F"{RED}<<== You already guessed that cell. Please choose a new one.{RESET}")
            continue

        # This is a valid, new guess
        already_guessed_cells.add((guessed_row, guessed_col))
        return guessed_row, guessed_col