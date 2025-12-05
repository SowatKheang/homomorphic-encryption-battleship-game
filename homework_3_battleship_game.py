
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
from core.constants.const import ALICE_NAME, BOB_NAME, BOAT_SIZES, YELLOW, BLUE, RED, GREEN, RESET
from core.helpers.paillier_helpers import generate_keypair
from core.helpers.board_helpers import create_board, place_boats, encrypt_board, print_player_board
from core.helpers.guess_helpers import do_valid_guess, do_homomorphic_guess

# 
# Main function
#
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
    
    #* Encrypting boards for both players
    print("Encrypting Alice's board...")
    encrypted_alice_board = encrypt_board(alice_board, alice_public_key)
    print("Alice's board encrypted.\n") 
    print("Encrypting Bob's board...")
    encrypted_bob_board = encrypt_board(bob_board, bob_public_key)
    print("Bob's board encrypted.\n")
    
    #* Game state variables
    alice_remaining_boat_cells = sum(BOAT_SIZES)
    bob_remaining_boat_cells = sum(BOAT_SIZES)
    
    #* Tracking guessed cells to avoid duplicates
    alice_guessed_cells = set()
    bob_guessed_cells = set()
    
    #* Game loop
    print("Starting the homomorphic Battleship game loop!\n")
    print("   - Board size: 10 x 10")
    print("   - Enter coordinates as (row, col) from 1 to 10.\n")
    is_alice_turn = True
    turn_counter = 0

    while alice_remaining_boat_cells > 0 and bob_remaining_boat_cells > 0:
        turn_counter += 1
        print(f"{YELLOW}--- Turn {turn_counter} ---{RESET}")
        
        if is_alice_turn:
            print(f"{BLUE}{ALICE_NAME}'s turn to guess!{RESET}")
            # Alice guesses on Bob's board
            guessed_row, guessed_col = do_valid_guess(ALICE_NAME, alice_guessed_cells)
            
            bob_remaining_boat_cells = do_homomorphic_guess(
                attacker_name=ALICE_NAME,
                defender_name=BOB_NAME,
                defender_public_key=bob_public_key,
                defender_private_key=bob_private_key,
                defender_plain_board=bob_board,
                defender_encrypted_board=encrypted_bob_board,
                defender_remaining_boat_cells=bob_remaining_boat_cells,
                guessed_row=guessed_row,
                guessed_col=guessed_col,
            )
        else:
            print(f"{BLUE}{BOB_NAME}'s turn to guess!{RESET}")
            # Bob guesses on Alice's board
            guessed_row, guessed_col = do_valid_guess(BOB_NAME, bob_guessed_cells)
            
            alice_remaining_boat_cells = do_homomorphic_guess(
                attacker_name=BOB_NAME,
                defender_name=ALICE_NAME,
                defender_public_key=alice_public_key,
                defender_private_key=alice_private_key,
                defender_plain_board=alice_board,
                defender_encrypted_board=encrypted_alice_board,
                defender_remaining_boat_cells=alice_remaining_boat_cells,
                guessed_row=guessed_row,
                guessed_col=guessed_col,
            )
            
        # Switch turn
        is_alice_turn = not is_alice_turn
    
    #* Game over, determine winner
    print(f"{RED}--- Game Over ---{RESET}")
    if alice_remaining_boat_cells == 0:
        print(f"{GREEN}{BOB_NAME} wins! All of {ALICE_NAME}'s ships have been sunk.{RESET}")
    else:
        print(f"{GREEN}{ALICE_NAME} wins! All of {BOB_NAME}'s ships have been sunk.{RESET}")
        
# 
# Entry point of the program
#
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame exited by user.")
        sys.exit()