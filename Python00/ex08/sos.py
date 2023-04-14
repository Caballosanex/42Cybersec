# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    sos.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alexsanc <alexsanc@student.42barcel>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/14 13:21:21 by alexsanc          #+#    #+#              #
#    Updated: 2023/04/14 13:37:12 by alexsanc         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys

MORSE_CODE_DICT = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
                   'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
                   'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
                   'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
                   'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
                   'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--',
                   '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
                   '9': '----.'}


def translate_toMorse(text):
    morse_code = ''
    for letter in text:
        if letter == ' ':
            morse_code += '/ '
        elif letter.upper() in MORSE_CODE_DICT:
            morse_code += MORSE_CODE_DICT[letter.upper()] + ' '
    return morse_code.strip()


if len(sys.argv) > 1:
    text = ' '.join(sys.argv[1:])
    morse_code = translate_toMorse(text)
    print(morse_code)
else:
    print('ERROR')
