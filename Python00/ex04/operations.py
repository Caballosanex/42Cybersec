# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    operations.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alexsanc <alexsanc@student.42barcel>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/11 19:11:17 by alexsanc          #+#    #+#              #
#    Updated: 2023/04/11 19:11:17 by alexsanc         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys

if len(sys.argv) != 3:
    print("2 Arguments Bro \n Us: python operations.py <n1> <n2> \n Exemple: \n \t python operations.py 10 3")
    sys.exit()
    
try:
	A = int(sys.argv[1])
	B = int(sys.argv[2])
except ValueError:
	print("Aixo no es un INT Bro")
	sys.exit()

sum_result = A + B
diff_result = A - B
prod_result = A * B
quot_result = None
rem_result = None

if B != 0:
    quot_result = A / B
    rem_result = A % B

print("Sum: ", sum_result)
print("Difference: ", diff_result)
print("Product: ", prod_result)

if quot_result is not None:
    print("Quotient: ", quot_result)
else:
    print("Quotient: ERROR - No puc dividir entre 0 Bro, go back to school")

if rem_result is not None:
    print("Remainder: ", rem_result)
else:
    print("Remainder: ERROR - No puc dividir entre 0 Bro, go back to school")