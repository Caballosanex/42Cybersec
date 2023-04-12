# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    count.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alexsanc <alexsanc@student.42barcel>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/11 14:45:15 by alexsanc          #+#    #+#              #
#    Updated: 2023/04/11 15:11:22 by alexsanc         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys

def text_analizer(text):
	
	if (len == 0):
		userInput = input("What is the text to analyse: ")
		
	if not isinstance(text, str):
		print ("Error: The argument is not a string")
		sys.exit()
		
	upperLetters = sum(1 for c in text if c.isupper())
	lowerLetters = sum(1 for c in text if c.islower())
	punctuation = sum(1 for c in text if c in str.punctuation)
	spaces = sum(1 for c in text if c.isspace())

	print("The text contains ", len(text), " characters:")
	print("Number of upper letters: ", upperLetters)
	print("Number of lower letters: ", lowerLetters)
	print("Number of punctuation marks: ", punctuation)
	print("Number of spaces: ", spaces)