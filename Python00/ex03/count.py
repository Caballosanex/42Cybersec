# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    count.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alexsanc <alexsanc@student.42barcel>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/11 14:45:15 by alexsanc          #+#    #+#              #
#    Updated: 2023/04/12 14:18:11 by alexsanc         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import string


def text_analyzer(text):
    if (len == 0):
        userInput = input("Bro, et falta text. Introdueix-lo: ")

    if not isinstance(text, str):
        print("Bro, això no és un string.")
        sys.exit()

    upperLetters = 0
    lowerLetters = 0
    punctuation = 0
    spaces = 0

    for char in text:
        if char.isupper():
            upperLetters += 1
        elif char.islower():
            lowerLetters += 1
        elif char.isspace():
            spaces += 1
        elif char in string.punctuation:
            punctuation += 1

    print("The text contains " + str(len(text)) + " characters:")
    print("- " + str(upperLetters) + " upper letter(s)")
    print("- " + str(lowerLetters) + " lower letter(s)")
    print("- " + str(punctuation) + " punctuation mark(s)")
    print("- " + str(spaces) + " space(s)")


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Error: Apren a posar les coses entre cometes dobles bro.")
    elif len(sys.argv) == 2:
        text_analyzer(sys.argv[1])
    else:
        userInput = input("Bro, et falta text. Introdueix-lo: ")
        text_analyzer(userInput)
