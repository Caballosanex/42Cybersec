# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    recipe.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alexsanc <alexsanc@student.42barcel>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/17 14:10:26 by alexsanc          #+#    #+#              #
#    Updated: 2023/04/20 16:32:11 by alexsanc         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

class Recipe:
    def __init__(self, name, cooking_lvl, cooking_time, ingredients, description="", recipe_type=""):
        self.name = name
        self.cooking_lvl = cooking_lvl
        self.cooking_time = cooking_time
        self.ingredients = ingredients
        self.description = description
        self.recipe_type = recipe_type

        if not isinstance(name, str) or not name:
            raise ValueError("Recipe name must be a non-empty string")
        if not isinstance(cooking_lvl, int) or cooking_lvl not in range(1, 6):
            raise ValueError(
                "Cooking level must be an integer between 1 and 5")
        if not isinstance(cooking_time, int) or cooking_time < 0:
            raise ValueError("Cooking time must be a positive integer")
        if not isinstance(ingredients, list) or not all(isinstance(i, str) for i in ingredients):
            raise ValueError("Ingredients must be a list of non-empty strings")
        if recipe_type not in ["starter", "lunch", "dessert"]:
            raise ValueError(
                "Recipe type must be one of 'starter', 'lunch', 'dessert' or an empty string")

    def __str__(self):
        txt = f"{self.name} ({self.cooking_lvl}/5, {self.cooking_time}min)\n"
        txt += f"Ingredients: {', '.join(self.ingredients)}\n"
        if self.description:
            txt += f"Description: {self.description}\n"
        if self.recipe_type:
            txt += f"Type: {self.recipe_type.capitalize()}\n"
        return txt
