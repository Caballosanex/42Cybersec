# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    whois.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alexsanc <alexsanc@student.42barcel>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/11 13:38:09 by alexsanc          #+#    #+#              #
#    Updated: 2023/04/11 13:56:48 by alexsanc         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys

if len(sys.argv) == 1:
	print("Has de posar un string. Fes: python3 exec.py 'algunacosa'")
	sys.exit()
	
if len(sys.argv) > 2:
    print("Bro, masses inputs. Un com a maxim")
    sys.exit()
    
num = sys.argv[1]

if num.isdigit() == False:
	print("Error: L'argument no es un enter")
	sys.exit()
    
if int(num) == 0:
	print("Gender issues. I'm Zero")
elif int(num) % 2 == 0:
	print("El numero es parell")
else:
	print("El numero es senar")