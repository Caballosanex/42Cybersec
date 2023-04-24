# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    generator.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alexsanc <alexsanc@student.42barcel>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/24 15:45:32 by alexsanc          #+#    #+#              #
#    Updated: 2023/04/24 16:28:47 by alexsanc         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

def generator(text, sep=" ", option=None):
    # Check if text argument is a string
    if not isinstance(text, str):
        yield "ERROR"
        return

    # Split the text into words using the sep parameter
    words = text.split(sep)

    # Perform option-specific actions on the words
    if option == "shuffle":
        # Use Fisher-Yates shuffle algorithm
        import random
        n = len(words)
        for i in range(n-1, 0, -1):
            j = random.randint(0, i)
            words[i], words[j] = words[j], words[i]
    elif option == "unique":
        words = list(set(words))
    elif option == "ordered":
        words.sort()
    elif option is not None:
        yield "ERROR"
        return

    # Yield each word
    for word in words:
        yield word
