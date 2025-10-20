# its a simple rock paper scissors game
# steps to play the game:
# 1. run the code
# 2. enter your name  
# 3. choose r for rock, p for paper, s for scissors
# 4. the computer will randomly choose its move
# 5. the winner will be declared
# 6. you can choose to play again or exit the game

import random

options = ['r', 'p', 's']

print("Welcome to Rock, Paper, Scissors Game!")
name = input("Enter your name: ")

# score counters
user_wins = 0
pc_wins = 0
ties = 0

while True:
    user_choice = input(f"Hello {name}, choose r for rock, p for paper, s for scissors: ").lower().strip()
    while user_choice not in options:
        user_choice = input("Invalid choice. Please enter r, p, or s: ").lower().strip()

    pc_choice = random.choice(options)
    print(f"Computer chose: {pc_choice}")

    if user_choice == pc_choice:
        print("It's a tie!")
        ties += 1
        
    elif (user_choice == 'r' and pc_choice == 's') or \
         (user_choice == 'p' and pc_choice == 'r') or \
         (user_choice == 's' and pc_choice == 'p'):
        print(f"Congratulations {name}, you win!")
        user_wins += 1
        
    else:
        print("Computer wins! Better luck next time.")
        pc_wins += 1

    play_again = input("Do you want to play again? (y/n): ").lower().strip()
    if play_again != 'y':
        print("Final score:")
        print(f"{name} wins: {user_wins}")
        print(f"Computer wins: {pc_wins}")
        print(f"Ties: {ties}")
        print("Thanks for playing!")
        break


# it is just for fun!