# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    test.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alexsanc <alexsanc@student.42barcel>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/20 17:51:42 by alexsanc          #+#    #+#              #
#    Updated: 2023/04/24 15:19:48 by alexsanc         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from vector import Vector
# Column vector of shape n * 1
v1 = Vector([[0.0], [1.0], [2.0], [3.0]])
v2 = v1 * 5
print(v2)
# Expected output:
# Vector([[0.0], [5.0], [10.0], [15.0]])
# Row vector of shape 1 * n
v1 = Vector([[0.0, 1.0, 2.0, 3.0]])
v2 = v1 * 5
print(v2)
# Expected output
# Vector([[0.0, 5.0, 10.0, 15.0]])
v2 = v1 / 2.0
print(v2)
# Expected output
# Vector([[0.0], [0.5], [1.0], [1.5]])
try:
    v1 / 0.0
except ZeroDivisionError as e:
    print(e)
# Expected ouput
# ZeroDivisionError: division by zero.
try:
    2.0 / v1
except NotImplementedError as e:
    print(e)
# Expected output:
# NotImplementedError: Division of a scalar by a Vector is not defined here.
# Column vector of shape (n, 1)
print(Vector([[0.0], [1.0], [2.0], [3.0]]).shape)
# Expected output
# (4,1)
print(Vector([[0.0], [1.0], [2.0], [3.0]]).values)
# Expected output
# [[0.0], [1.0], [2.0], [3.0]]
# Row vector of shape (1, n)
print(Vector([[0.0, 1.0, 2.0, 3.0]]).shape)
# Expected output
# (1,4)
print(Vector([[0.0, 1.0, 2.0, 3.0]]).values)
# Expected output
# [[0.0, 1.0, 2.0, 3.0]]
# Example 1:
v1 = Vector([[0.0], [1.0], [2.0], [3.0]])
print(v1.shape)

print(v1.T())
# Expected output:
# Vector([[0.0, 1.0, 2.0, 3.0]])
print(v1.T().shape)
# Expected output:
# (1,4)
# Example 2:
v2 = Vector([[0.0, 1.0, 2.0, 3.0]])
print(v2.shape)
# Expected output:
# (1,4)
print(v2.T())
# Expected output:
# Vector([[0.0], [1.0], [2.0], [3.0]])
print(v2.T().shape)
# Expected output:
# (4,1)
# Example 1:
v1 = Vector([[0.0], [1.0], [2.0], [3.0]])
v2 = Vector([[2.0], [1.5], [2.25], [4.0]])
print(v1.dot(v2))
# Expected output:
# 18.0
v3 = Vector([[1.0, 3.0]])
v4 = Vector([[2.0, 4.0]])
print(v3.dot(v4))
print(v1)
# Expected output: to see what __str__() should do
# [[0.0, 1.0, 2.0, 3.0]]
