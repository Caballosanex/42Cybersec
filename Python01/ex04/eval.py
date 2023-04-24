# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    eval.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alexsanc <alexsanc@student.42barcel>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/24 16:28:32 by alexsanc          #+#    #+#              #
#    Updated: 2023/04/24 16:29:32 by alexsanc         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

class Evaluator:
    @staticmethod
    def zip_evaluate(coefs, words):
        if len(coefs) != len(words):
            return -1
        return sum([len(word) * coef for word, coef in zip(words, coefs)])

    @staticmethod
    def enumerate_evaluate(coefs, words):
        if len(coefs) != len(words):
            return -1
        return sum([len(word) * coefs[i] for i, word in enumerate(words)])
