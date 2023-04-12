# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    kata03.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alexsanc <alexsanc@student.42barcel>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/12 14:22:59 by alexsanc          #+#    #+#              #
#    Updated: 2023/04/12 15:19:58 by alexsanc         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# Put this at the top of your kata03.py file
kata = "The right format"

# Add hyphens to the left of the string to create a 42 character long line
# 1. "-" * (42 - len(kata)) creates a string with 42 - len(kata) hyphens
# 2. "-" * (42 - len(kata)) + kata creates a string with 42 - len(kata) hyphens
# and kata appended to it """
formatted_kata = "-" * (42 - len(kata)) + kata

# Print the formatted string and delete $ tracer
print(formatted_kata, end="")
