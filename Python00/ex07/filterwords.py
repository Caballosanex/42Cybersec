# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    filterwords.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alexsanc <alexsanc@student.42barcel>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/14 13:13:27 by alexsanc          #+#    #+#              #
#    Updated: 2023/04/14 13:19:20 by alexsanc         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import string
import sys

if len(sys.argv) != 3:
    print("ERROR")
    sys.exit(1)

try:
    S = sys.argv[1]
    N = int(sys.argv[2])
except ValueError:
    print("Error: second argument must be an integer")
    sys.exit(1)

punctuation = string.punctuation

words = [word.translate(str.maketrans("", "", punctuation)) for word in S.split()]

result = [word for word in words if len([c for c in word if c not in punctuation]) > N]

print(result)
