# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    guess.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alexsanc <alexsanc@student.42barcel>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/14 13:55:50 by alexsanc          #+#    #+#              #
#    Updated: 2023/04/17 15:27:45 by alexsanc         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import random

# generate a random number between 1 and 99
secret_number = random.randint(1, 99)

# initialize the number of trials to 0
num_trials = 0

# loop until the user guesses the correct number or types 'exit'
while True:
    # ask the user to input their guess
    user_input = input(
        "Guess a number between 1 and 99 (or type 'exit' to quit): ")

    # check if the user wants to quit
    if user_input.lower() == 'exit':
        print("Goodbye! The secret number was", secret_number)
        break

    num_trials += 1

    # check if the user's input is a valid integer
    try:
        guess = int(user_input)
    except ValueError:
        print("Invalid input. Please enter an integer between 1 and 99.")
        continue

    # check if the user's guess is correct
    if guess == secret_number:
        if num_trials == 1:
            print("Congratulations! You guessed the secret number on your first try!")
        else:
            print("Congratulations! You guessed the secret number in",
                  num_trials, "tries.")

        if secret_number == 42:
            print("The number 42 is the answer to the ultimate question of life, the universe, and everything.")

        break
    elif guess < secret_number:
        print("Your guess is too low. Try again.")
    else:
        print("Your guess is too high. Try again.")
