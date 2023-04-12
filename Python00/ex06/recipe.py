# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    recipe.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alexsanc <alexsanc@student.42barcel>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/12 16:02:20 by alexsanc          #+#    #+#              #
#    Updated: 2023/04/12 19:11:04 by alexsanc         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import string

cookbook = {
    "Sandwich": {
        "ingredients": ["ham", "bread", "cheese", "tomatoes"],
        "meal": "lunch",
        "prep_time": 10
    },
    "Cake": {
        "ingredients": ["flour", "sugar", "eggs"],
        "meal": "dessert",
        "prep_time": 60
    },
    "Salad": {
        "ingredients": ["avocado", "arugula", "tomatoes", "spinach"],
        "meal": "lunch",
        "prep_time": 15
    }
}


def print_recipeName():
    for key in cookbook:
        print(key)


def print_recipeDetails(recipe):
    if recipe in cookbook:
        print("Recipe for " + recipe + ":")
        print("Ingredients list: " + str(cookbook[recipe]["ingredients"]))
        print("To be eaten for " + cookbook[recipe]["meal"] + ".")
        print("Takes " + str(cookbook[recipe]
              ["prep_time"]) + " minutes of cooking.")
    else:
        print("This recipe does not exist")


def delete_recipe():
    print("Which recipe do you want to delete?")
    recipe = input()
    if recipe in cookbook:
        del cookbook[recipe]
        print("Recipe deleted successfully")
    else:
        print("This recipe does not exist")


def add_userRecipe():
    print("Enter a name")
    name = input()
    print("Enter ingredients")
    ingredients = input()
    print("Enter a meal type")
    meal = input()
    print("Enter a preparation time")
    prep_time = input()
    cookbook[name] = {
        "ingredients": ingredients,
        "meal": meal,
        "prep_time": prep_time
    }
    print("Recipe added successfully")


if __name__ == "__main__":
    option = "-1"
    while option != "5":
        print("Welcome to the Python Cookbook!\n")
        print("\tList of available options:\n")
        print("\t1: Add a recipe")
        print("\t2: Delete a recipe")
        print("\t3: Print a recipe")
        print("\t4: Print the cookbook")
        print("\t5: Quit\n")
        print("Please select an option:\n")
        option = input()
        if option == "1":
            add_userRecipe()
        elif option == "2":
            delete_recipe()
        elif option == "3":
            print("Please enter a recipe name to get its details:")
            recipe = input()
            print_recipeDetails(recipe)
        elif option == "4":
            print_recipeName()
        if option == "5":
            print("Cookbook closed. Goodbye!")
        if option not in ["1", "2", "3", "4", "5"]:
            print("This option does not exist, please type the corresponding number.")
            print("To exit, enter 5.")
