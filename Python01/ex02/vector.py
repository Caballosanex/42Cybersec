# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    vector.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alexsanc <alexsanc@student.42barcel>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/20 17:52:39 by alexsanc          #+#    #+#              #
#    Updated: 2023/04/24 16:28:56 by alexsanc         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

class Vector:
    def __init__(self, values):
        self.values = values
        self.shape = (len(values), 1) if isinstance(
            values[0], list) else (1, len(values))

    def __repr__(self):
        return f'Vector({self.values})'

    def __add__(self, other):
        if self.shape != other.shape:
            raise ValueError('Cannot add vectors of different shapes')
        return Vector([[a+b for a, b in zip(x, y)] for x, y in zip(self.values, other.values)])

    def __sub__(self, other):
        if self.shape != other.shape:
            raise ValueError('Cannot subtract vectors of different shapes')
        return Vector([[a-b for a, b in zip(x, y)] for x, y in zip(self.values, other.values)])

    def __mul__(self, other):
        return Vector([[a*other for a in x] for x in self.values])

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if other == 0:
            raise ZeroDivisionError('Cannot divide by zero')
        return Vector([[a/other for a in x] for x in self.values])

    def __rtruediv__(self, other):
        raise NotImplementedError(
            'Division of a scalar by a Vector is not defined here')

    def dot(self, other):
        if self.shape != other.shape:
            raise ValueError(
                "Both vectors must have the same shape to calculate the dot product")
        result = 0
        for i in range(len(self.values)):
            for j in range(len(self.values[i])):
                result += self.values[i][j] * other.values[i][j]
        return result

    def T(self):
        return Vector([list(t) for t in zip(*self.values)])
