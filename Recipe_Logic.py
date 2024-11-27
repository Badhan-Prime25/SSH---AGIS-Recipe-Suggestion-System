import re
import sqlite3 as lite

import csv

#import os

# Connects to the recipe Database
recipesDatabase = lite.connect('foodDatabase.db')
repCur = recipesDatabase.cursor()

class Recipe:
    def __init__(self, name, instructions, ingredients, meal_type, prep_time, veg):
        self.name = name
        self.ingredients = ingredients
        self.meal_type = meal_type
        self.instructions = ""
        if veg == 1:
            self.vegetarian = "Veg"
        else:
            self.vegetarian = "Non-Veg"
        self.prep_time = str(prep_time) + " minutes"
        instructionsSplitter  = instructions.split(".")
        i = 1
        for instruction in instructionsSplitter:
            if instruction.strip():
                self.instructions = self.instructions+str(i)+". " +instruction.strip() +"\n"
                i += 1


def split_ingredient(ingredient):
    # Regex to match the quantity and unit at the start of the string
    match = re.match(r"(\d+\s*[^\d\s]*)\s+(.*)", ingredient)
    if match:
        quantity_unit = match.group(1)  # Quantity and unit (e.g., "1 tsp")
        ingredient_name = match.group(2)  # Ingredient name (e.g., "olive oil")
        return [quantity_unit, ingredient_name]
    else:
        # If the string doesn't match the expected format, return it as-is
        return [ingredient, ""]

def get_recipes():
    # SQL statement to get required data
    recipe_sql = """
                    SELECT 
                        r.recipe_name,
                        r.instructions,
                        GROUP_CONCAT(ri.quantity || ' ' || i.ingredient_name) AS ingredients,
                        r.meal_type,
                        r.prep_time,
                        r.veg_status
                    FROM
                        Recipes AS r
                    JOIN 
                        Recipe_Ingredient AS ri ON r.recipe_id = ri.recipe_id
                    JOIN 
                        Ingredients AS i ON ri.ingredient_id = i.ingredient_id
                    GROUP BY  r.recipe_name, r.instructions, r.meal_type
        """
    repCur.execute(recipe_sql) # executes SQL Statement
    rows = repCur.fetchall()
    recipes =[]
    # Makes an instance for each recipe
    for row in rows:
        name,instructions,ingredients_list,meal_type,prep_time,veg = row
        ingredients_list = ingredients_list.split(',')
        ingredients_2d = [split_ingredient(ingredient) for ingredient in ingredients_list]
        recipes.append(Recipe(name, instructions, ingredients_2d, meal_type,prep_time,veg))
    return recipes # Returns a lists of instances



def extract_ingredients(file_path):
    ingredients = []
    with open(file_path, mode='r') as file:
        csv_file = csv.reader(file, delimiter=',')
        next(csv_file)  # Skip the header row
        for row in csv_file:
            amount = row[0].strip()
            ingredient = row[1].strip()
            ingredients.append([amount,ingredient])
        return ingredients

def match_ingredients(recipes, available_ingredients):
    possible_recipes = []
    partial_recipes = []

    for recipe in recipes:
        required_ingredients = recipe.ingredients  # 2D array: [[required_amount, ingredient_name], ...]
        matched_ingredients = 0  # Initialize outside the loop over required_ingredients

        for required_amount, ingredient_name in required_ingredients:
            # Search for the ingredient in available_ingredients
            for available_quantity, available_name in available_ingredients:
                if available_name == ingredient_name:
                    if available_quantity >= required_amount:
                        matched_ingredients += 1
                    break  # Stop searching since we found the ingredient
            else:
                # Ingredient not found in available_ingredients
                continue  # You may want to handle this case differently

        total_ingredients = len(required_ingredients)
        match_ratio = matched_ingredients / total_ingredients

        if match_ratio == 1.0:
            possible_recipes.append(recipe)
        elif match_ratio >= 0.80 or (total_ingredients -1 == matched_ingredients):
            partial_recipes.append(recipe)
    return possible_recipes,partial_recipes

# Example usage:



    # for

    # for recipe in recipes:
    #     no_ingredients = len(recipe.ingredients)
    #     matching_ingredients = []
    #     for ingredient in ingredients_list:
    #         if ingredient in recipe.ingredients:
    #             matching_ingredients.append(ingredient)
    #     if len(matching_ingredients) == no_ingredients:
    #         possible_recipes.append(recipe)
    #     elif len(matching_ingredients) >= no_ingredients * 0.8:
    #         partial_recipes.append(recipe)
    # print(possible_recipes)
    # print(partial_recipes)



