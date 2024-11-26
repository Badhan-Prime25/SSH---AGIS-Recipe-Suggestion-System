import sqlite3 as lite
import csv
#import os

# Connects to the recipe Database
recipesDatabase = lite.connect('foodDatabase.db')
repCur = recipesDatabase.cursor()

class Recipe:
    def __init__(self, name, instructions, ingredients, meal_type,prep_time):
        self.name = name
        self.instructions = instructions
        self.ingredients = ingredients
        self.meal_type = meal_type
        #self.vegetarian = vegetarian Database does not have any column with these values
        self.prep_time = prep_time

def get_recipes():
    # SQL statement to get required data
    recipe_sql = """
                    SELECT 
                        r.recipe_name,
                        r.instructions,
                        GROUP_CONCAT (i.ingredient_name) AS ingredients,
                        r.meal_type,
                        r.prep_time
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
        name,instructions,ingredients_list,meal_type,prep_time = row
        ingredients_list = ingredients_list.split(',')
        recipes.append(Recipe(name, instructions, ingredients_list, meal_type,prep_time))
    return recipes # Returns a lists of instances


def extract_ingredients():
    ingredients = []
    with open('ENTER_CSV_FILE.csv', mode = 'r') as file:
        csv_file = csv.reader(file, delimiter=',')
        for row in csv_file:
            ingredients.extend(row)
    return ingredients




def match_ingredients(recipes, ingredients):
    possible_recipes = []
    partial_recipes = []
    ingredients_list = ingredients.split(',')
    for recipe in recipes:
        no_ingredients = len(recipe.ingredients)
        matching_ingredients = []
        for ingredient in ingredients_list:
            if ingredient in recipe.ingredients:
                matching_ingredients.append(ingredient)
        if len(matching_ingredients) == no_ingredients:
            possible_recipes.append(recipe)
        elif len(matching_ingredients) >= no_ingredients * 0.8:
            partial_recipes.append(recipe)
    print(possible_recipes)
    print(partial_recipes)
