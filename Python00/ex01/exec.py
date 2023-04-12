# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    exec.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alexsanc <alexsanc@student.42barcel>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/11 13:35:08 by alexsanc          #+#    #+#              #
#    Updated: 2023/04/12 14:58:16 by alexsanc         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys


if len(sys.argv) == 1:
    print("Has de posar un string. Fes: python3 exec.py 'algunacosa'")
else:
    print(' '.join(sys.argv[1:])[::-1].swapcase())
