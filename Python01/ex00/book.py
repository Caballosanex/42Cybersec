# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    book.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alexsanc <alexsanc@student.42barcel>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/17 14:10:21 by alexsanc          #+#    #+#              #
#    Updated: 2023/04/20 17:12:19 by alexsanc         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from datetime import datetime
from recipe import Recipe


class Book:
    def __init__(self, name):
        self.name = name
        self.last_update = datetime.now()
        self.creation_date = datetime.now()
        self.recipes_list = {"starter": [], "lunch": [], "dessert": []}

    def get_recipe_by_name(self, name):
        for recipes in self.recipes_list.values():
            for recipe in recipes:
                if recipe.name == name:
                    print(recipe)
                    return recipe
        print(f"No recipe found with name '{name}'")
        return None

    def get_recipes_by_types(self, recipe_type):
        recipes = self.recipes_list.get(recipe_type, [])
        for recipe in recipes:
            print(recipe.name)
        return recipes

    def add_recipe(self, recipe):
        if not isinstance(recipe, Recipe):
            raise ValueError("You can only add Recipe objects to the book")
        self.recipes_list[recipe.recipe_type].append(recipe)
        self.last_update = datetime.now()
