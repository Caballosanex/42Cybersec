# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    vector.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alexsanc <alexsanc@student.42barcel>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/20 17:52:39 by alexsanc          #+#    #+#              #
#    Updated: 2023/04/20 17:52:41 by alexsanc         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

class Vector:
    def __init__(self, values):
        self.values = values
        if len(values) == 1:
            self.shape = (1, len(values[0]))
        else:
            self.shape = (len(values), 1)

    def __str__(self):
        return "Vector({})".format(self.values)

    def __add__(self, other):
        if self.shape != other.shape:
            raise ValueError("Vectors must have the same shape")
        values = []
        for i in range(len(self.values)):
            row = []
            for j in range(len(self.values[0])):
                row.append(self.values[i][j] + other.values[i][j])
            values.append(row)
        return Vector(values)

    def __sub__(self, other):
        if self.shape != other.shape:
            raise ValueError("Vectors must have the same shape")
        values = []
        for i in range(len(self.values)):
            row = []
            for j in range(len(self.values[0])):
                row.append(self.values[i][j] - other.values[i][j])
            values.append(row)
        return Vector(values)

    def __mul__(self, other):
        values = []
        for i in range(len(self.values)):
            row = []
            for j in range(len(self.values[0])):
                row.append(self.values[i][j] * other)
            values.append(row)
        return Vector(values)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if other == 0:
            raise ZeroDivisionError("Division by zero")
        values = []
        for i in range(len(self.values)):
            row = []
            for j in range(len(self.values[0])):
                row.append(self.values[i][j] / other)
            values.append(row)
        return Vector(values)

    def __rtruediv__(self, other):
        raise NotImplementedError(
            "Division of a scalar by a Vector is not defined here")

    def dot(self, other):
        if self.shape != other.shape:
            raise ValueError("Vectors must have the same shape")
        result = 0.0
        for i in range(len(self.values)):
            for j in range(len(self.values[0])):
                result += self.values[i][j] * other.values[i][j]
        return result

    def T(self):
        values = []
        if len(self.values) == 1:
            for j in range(len(self.values[0])):
                row = [self.values[0][j]]
                values.append(row)
        else:
            for j in range(len(self.values[0])):
                row = []
                for i in range(len(self.values)):
                    row.append(self.values[i][j])
                values.append(row)
        return Vector(values)
