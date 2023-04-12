# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    kata02.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alexsanc <alexsanc@student.42barcel>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/11 19:53:58 by alexsanc          #+#    #+#              #
#    Updated: 2023/04/11 19:53:58 by alexsanc         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# Put this at the top of your kata02.py file
kata = (2019, 9, 25, 3, 30)

print("{:02d}/{:02d}/{:d} {:02d}:{:02d}".format(kata[1], kata[2], kata[0], kata[3], kata[4]))

""" kata es una tupla que contiene cinco valores enteros (2019, 9, 25, 3, 30). Las tuplas son secuencias inmutables en Python, y cada elemento en la tupla representa un valor específico, como año, mes, día, hora y minuto, respectivamente.

Se llama al método .format() en una cadena con marcadores de posición {} para indicar dónde se insertarán los valores.

Dentro de los marcadores de posición {}, tenemos marcadores de posición con diferentes formatos:

:02d - Este es un especificador de formato para un entero (d). Indica que el entero se imprimirá con al menos dos dígitos (2) y se agregarán ceros a la izquierda si el entero tiene menos de dos dígitos (0).
:d - Este es un especificador de formato para un entero (d). Indica que el entero se imprimirá sin ceros a la izquierda.
El método .format() toma los valores de la tupla kata e los inserta en los marcadores de posición en la cadena en el orden en que aparecen. Los valores se insertan de manera secuencial, correspondiendo a los marcadores de posición.

La cadena resultante se imprime utilizando la función print().

Por lo tanto, la salida del código será una cadena formateada que representa los valores en la tupla kata de la siguiente manera: 09/25/2019 03:30. Ten en cuenta que se agregan ceros a la izquierda en los valores de mes, día y hora para asegurarse de que tengan al menos dos dígitos, como se especifica en los marcadores de posición. """
