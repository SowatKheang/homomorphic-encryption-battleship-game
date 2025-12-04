
"""
Applied Cryptograpy II  :   Homework 3 Battleship game.
Student                 :   Sowat Kheang
Howework 3              :   Implementing a full Battleship board 10x10 matrix and each player 
                            has 5 boats with sizes of 5, 4, 3, 2 and 2 dots using homomorphic encryption 
                            to hide the board information
                        
Run the program         :   1. uv sync
                            2. uv run homework_3_battleship_game.py
"""

import random
import sys
from phe import paillier
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

# Encrypt the board with Paillier public key
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

# Generate Paillier keypair
def generate_keypair(n_length=512):
    """
        Generate a Paillier keypair with the specified key length.
        Returns the public and private keys.
    """
    public_key, private_key = paillier.generate_paillier_keypair(n_length=n_length)
    return public_key, private_key

# Main function
def main():
    print(f"\nWelcome to the Battleship Game with Homomorphic Encryption\n")
    
    # Optional: fix random seed so boat positions are deterministic for demo
    random.seed(23)
    
    # Alice's keypair
    print("Generating Paillier keypair for Alice...")
    alice_public_key, alice_private_key = generate_keypair(n_length=256)  # small key for demo
    print("Alice's Paillier keypair generated.\n")
    
    # Bob's keypair
    print("Generating Paillier keypair for Bob...")
    bob_public_key, bob_private_key = generate_keypair(n_length=256)      # small key for demo
    print("Bob's Paillier keypair generated.\n")
    
    # Creating boards
    print("Creating and placing boats on Alice's board...")
    alice_board = create_board()
    bob_board = create_board()
    place_boats(alice_board)
    place_boats(bob_board)
    
    #! For demo purposes, displaying plain boards
    #! Need to remove this is a real game
    print_player_board(alice_board, "Alice")
    print_player_board(bob_board, "Bob")

# Print player board helper function
def print_player_board(player_board, player_name):
    print(f"\033[93m<<== [DEBUG] {player_name}'s plain board (1 = boat, 0 = empty):\033[0m")
    for row in player_board:
        # if item in row is 1, print blue else print white
        print("   ", end="")
        for item in row:
            if item == 1:
                print("\033[94m1\033[0m", end=" ") # This code prints in blue color
            else:
                print("0", end=" ")
        print()
    print()
    
# TODO: Implement Encrypting boards

# TODO: Implement Players taking turns to guess


# Entry point
if __name__ == "__main__":
    main()