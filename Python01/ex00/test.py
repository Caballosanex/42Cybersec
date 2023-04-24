# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    test.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alexsanc <alexsanc@student.42barcel>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/17 14:10:28 by alexsanc          #+#    #+#              #
#    Updated: 2023/04/20 17:52:25 by alexsanc         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
from book import Book
from recipe import Recipe

sys.tracebacklimit = 0

r1 = Recipe('Spaghetti Carbonara', 4, 30, ['spaghetti', 'bacon', 'eggs', 'parmesan'], 'Delicious pasta!', 'starter')
r2 = Recipe('Chocolate Cake', 5, 60, ['flour', 'sugar', 'cocoa powder', 'eggs', 'milk', 'butter'], 'Decadent dessert', 'dessert')
r3 = Recipe('Caesar Salad', 2, 15, ['romaine lettuce', 'croutons', 'parmesan cheese', 'caesar dressing'], 'Classic salad', 'lunch')

my_cookbook = Book('My Cookbook')

my_cookbook.add_recipe(r1)
my_cookbook.add_recipe(r2)
my_cookbook.add_recipe(r3)

print(my_cookbook.get_recipe_by_name('Chocolate Cake'))

print(my_cookbook.get_recipes_by_types('lunch'))

print(my_cookbook.last_update)

print(my_cookbook.creation_date)

print(my_cookbook)

print(repr(my_cookbook))

# Output:
# Chocolate Cake (5/5, 60min)
# Ingredients: flour, sugar, cocoa powder, eggs, milk, butter
# Description: Decadent dessert
# Recipe type: dessert
# [Chocolate Cake (5/5, 60min)]
# 2023-04-20 16:57:49.000000
# 2023-04-17 14:10:28.000000
# My Cookbook cookbook, last updated 2023-04-20 16:57:49.000000, created 2023-04-17 14:10:28.000000

# My Cookbook cookbook, last updated 2023-04-20 16:57:49.000000, created 2023-04-17 14:10:28.000000

# **************************************************************************** #
