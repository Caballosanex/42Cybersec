# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    kata01.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alexsanc <alexsanc@student.42barcel>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/11 19:50:29 by alexsanc          #+#    #+#              #
#    Updated: 2023/04/11 19:50:29 by alexsanc         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# Put this at the top of your kata01.py file
kata = {
'Python': 'Guido van Rossum',
'Ruby': 'Yukihiro Matsumoto',
'PHP': 'Rasmus Lerdorf',
}

for key in kata:
	print(key, "was created by", kata[key])