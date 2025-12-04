
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
from core.helpers.board_helpers import create_board, place_boats, encrypt_board, print_player_board
from core.helpers.paillier_helpers import generate_keypair
from core.constants.const import ALICE_NAME, BOB_NAME

# Main function
def main():
    print(f"\nWelcome to the Battleship Game with Homomorphic Encryption\n")
    
    #? Optional: fix random seed so boat positions are deterministic for demo
    random.seed(23)
    
    #* Alice's keypair
    print("Generating Paillier keypair for Alice...")
    alice_public_key, alice_private_key = generate_keypair(n_length=256)  # small key for demo
    print("Alice's Paillier keypair generated.\n")
    
    #* Bob's keypair
    print("Generating Paillier keypair for Bob...")
    bob_public_key, bob_private_key = generate_keypair(n_length=256)      # small key for demo
    print("Bob's Paillier keypair generated.\n")
    
    #* Creating boards for both players
    print("Creating and placing boats on Alice's board...")
    alice_board = create_board()
    bob_board = create_board()
    
    #* Placing boats for both players
    place_boats(alice_board)
    place_boats(bob_board)
    
    #! For demo purposes, displaying plain boards
    #! Need to remove this is a real game
    print_player_board(alice_board, ALICE_NAME)
    print_player_board(bob_board, BOB_NAME)

# 
# Entry point of the program
#
if __name__ == "__main__":
    main()