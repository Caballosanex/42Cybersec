# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    loading.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alexsanc <alexsanc@student.42barcel>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/14 14:11:12 by alexsanc          #+#    #+#              #
#    Updated: 2023/04/14 14:27:00 by alexsanc         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import time


def ft_progress(listy):
    total = len(listy)
    for i, item in enumerate(listy):
        progress = i / total * 100
        eta = (total - i) * 0.01
        yield item
        print(
            f"ETA: {eta:.2f}s [{progress:3.0f}%][{'='*int(progress/10)}>{' '*(10-int(progress/10))}] {i}/{total}", end="\r")


"""
1. f before the string: this is the new way to format strings in python 3.6+
2. \r: this is to return to the start of the line
3. {eta:.2f}: the eta value will be formatted as a float with 2 decimals
4. {progress:3.0f}: the progress value will be formatted as a float with 3 characters and 0 decimals
5. {int(progress/10)}: this will be the number of '=' to print
6. {10-int(progress/10))}: this will be the number of spaces to print
7. {i}/{total}: the current iteration and the total number of iterations
8. {elapsed:.2f}: the elapsed time formatted as a float with 2 decimals
9. end="": this is to remove the new line at the end of the print() function
"""

listy = range(1000)
ret = 0
for elem in ft_progress(listy):
    ret += (elem + 3) % 5
    time.sleep(0.01)
print()
print(ret)

listy = range(3333)
ret = 0
for elem in ft_progress(listy):
    ret += elem
    time.sleep(0.005)
print()
print(ret)
