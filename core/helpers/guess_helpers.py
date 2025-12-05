
import random
from core.constants.const import BOARD_SIZE, BOAT_SIZES, RED, BLUE, GREEN, YELLOW, RESET

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
    
#
# Homomorphic guess processing
#
def do_homomorphic_guess(
    attacker_name, # Alice or Bob
    defender_name, # Same as above
    defender_public_key, # Paillier public key
    defender_private_key, # Paillier private key
    defender_plain_board, # 10x10 matrix with 0/1 
    defender_encrypted_board, # 10x10 matrix with ciphertexts
    defender_remaining_boat_cells, # integer count for remaining boat cells
    guessed_row,
    guessed_col,
):
    # Convert zero-based indices to human-friendly 1–10 for printing
    human_row = guessed_row + 1
    human_col = guessed_col + 1
    
    # Encrypted ciphertext at guessed position
    encrypted_cell = defender_encrypted_board[guessed_row][guessed_col]
    
    # Homomorphic subtraction: encrypted_cell - 1 for checking hit/miss
    encrypted_difference = encrypted_cell - 1
    
    # Blinding factor to hide magnitude of the decrypted result
    blinding_factor = random.randint(1, 999999)
    encrypted_result = encrypted_difference * blinding_factor
    
    # Decrypt only the blinded result
    decrypted_result = defender_private_key.decrypt(encrypted_result)
    
    # Display result for this blinded value
    print(f"{YELLOW}[{defender_name} Decrypts] Blinded result = {decrypted_result}{RESET}")
    
    # Determine hit or miss based on decrypted result
    if decrypted_result == 0:
        print(
            f"{GREEN}==>> HIT! {attacker_name} hit {defender_name}'s ship at{RESET}"
            f"{GREEN}({human_row}, {human_col}) <<=={RESET}"
        )
        
        # This is a hit, update defender's state
        defender_plain_board[guessed_row][guessed_col] = -1
        
        # Re-encrypt this cell as 0, so future hits on same cell don't reduce count again
        defender_encrypted_board[guessed_row][guessed_col] = defender_public_key.encrypt(0)

        defender_remaining_boat_cells -= 1
        
    else:
        # Any non-zero decrypted value is treated as random noise -> MISS
        print(
            f"{RED}<<== MISS {attacker_name} did not hit a ship at {RESET}"
            f"{RED}({human_row}, {human_col}) <<=={RESET}"
        )
        
    print(f"{BLUE}[{defender_name}] Remaining ship cells: {defender_remaining_boat_cells}{RESET}")
    print("-" * 50)

    return defender_remaining_boat_cells
    