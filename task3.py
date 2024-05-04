import sys
import random
import hmac
import hashlib
from tabulate import tabulate
import secrets

class KeyGenerator:
    @staticmethod
    def generate_key():
        return secrets.token_bytes(32)  # 256 bits key

class HMACCalculator:
    @staticmethod
    def calculate_hmac(message, key):
        return hmac.new(key, message.encode('utf-8'), hashlib.sha3_256).hexdigest()

class RuleDeterminer:
    def sign(num):
        if num > 0:
            return 1
        elif num < 0:
            return -1
        else:
            return 0
    
    @staticmethod
    def determine_winner(user_move, computer_move, moves):
        index1 = moves.index(user_move)
        index2 = moves.index(computer_move)
        n = len(moves)
        half = n // 2

        winer = RuleDeterminer.sign(((index1 - index2 + half + n) % n) - half)
        if winer == 1: return "Computer win!"
        elif winer == -1: return "You win!"
        else: return "Draw"
        

class TableGenerator:
    @staticmethod
    def generate_table(moves):
        table = [['v PC\\User >'] + moves]
        for move in moves:
            row = [move]
            for opponent in moves:
                if move == opponent:
                    row.append('Draw')
                else:
                    result = RuleDeterminer.determine_winner(move, opponent, moves)
                    if result == 'Computer win!': row.append('Lose')
                    elif result == 'You win!': row.append('Win')
                    else: row.append('Draw')
            table.append(row)

        return tabulate(table, headers="firstrow", tablefmt="grid")

def main():
    moves = sys.argv[1:]
    
    # Checking if the number of arguments is odd and greater than or equal to 3
    if len(moves) % 2 == 0 or len(moves) < 3:
        print("\nError: Please provide an odd number of non-repeating strings must be >= 3.")
        print("Example: python task3.py Rock Paper Scissors.\n")
        return
    
    # Checking for duplicate moves
    if len(set(moves)) != len(moves):
        print("\nError: Please provide non-repeating strings as moves.\n")
        return
    
    key = KeyGenerator.generate_key()
    computer_move = random.choice(moves)
    computer_hmac = HMACCalculator.calculate_hmac(computer_move, key)

    print("HMAC: ", computer_hmac)
    print("Available moves:")

    for i, move in enumerate(moves):
        print(f"{i+1} - {move}")
    print("0 - Exit")
    print("? - help")

    try:
        user_input = input("Enter your move: ")
        
        if user_input == "?":
            print('This table is generate the states that the game results are from user point of view.')
            print(TableGenerator.generate_table(moves))
            return
        
        user_choice = int(user_input)

        if user_choice == 0:
            print("Exiting...")
            return
        elif user_choice < 0 or user_choice > len(moves):
            print("Invalid choice. Please enter a valid number by following the moves.\n")
        else:
            user_move = moves[user_choice - 1]
            print("Your move:", user_move)

            if(computer_hmac == HMACCalculator.calculate_hmac(computer_move, key)):
                print("Computer move:", computer_move)
            else:
                print("Computer might not have played fair.\n")
                return 
            
            winner = RuleDeterminer.determine_winner(user_move, computer_move, moves)
            print(winner)
            print("HMAC key: ", key.hex())
            print("Fair play.\n")

    except ValueError:
        print("Invalid input. Please enter a number.\n")

if __name__ == "__main__":
    main()
