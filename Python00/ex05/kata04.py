# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    kata04.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alexsanc <alexsanc@student.42barcel>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/12 14:42:45 by alexsanc          #+#    #+#              #
#    Updated: 2023/04/12 16:02:00 by alexsanc         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# Put this at the top of your kata04.py file
kata = (0, 4, 132.42222, 10000, 12345.67)

# Extract the values from the tuple
a, b, c, d, e = kata

# Format the values according to the specified format
formatted_a = f"{a:02}"
formatted_b = f"{b:02}"
formatted_c = f"{c:.2f}"
formatted_d = f"{d:.2e}"
formatted_e = f"{e:.2e}"

# Print the formatted string to the console
print(f"module_{formatted_a}, ex_{formatted_b} : {formatted_c}, {formatted_d}, {formatted_e}")
