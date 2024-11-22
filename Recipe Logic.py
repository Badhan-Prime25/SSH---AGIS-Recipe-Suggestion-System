import sqlite3 as lite
import csv
import os

# Connects to the recipe Database
recipesDatabase = lite.connect('foodDatabase.db')
repCur = recipesDatabase.cursor()

def get_recipes():
    recipe_sql = """""
                SELECT 
                    r.recipe_name,
                    r.instructions,
                    ri.ingredients,
                    r.meal_type,
                    r.veg_status,
                    r.prep_time AS duration
                FROM
                    Recipe AS r
                JOIN 
                    Recipe_Ingredient AS ri ON r.recipe_id = ri.recipe_id
                JOIN 
                    Ingredients AS i ON ri.ingredient_id = i.ingredient_id
                GROUP BY  r.recipe_name,r.instructions,ri.ingredients,r.meal_type,r.veg_status,r.prep_time AS duration
    """""
    repCur.execute(recipe_sql)
    recipes = repCur.fetchall()
    return recipes

def extract_ingredients():
    ingredients = []
    with open('ENTER_CSV_FILE.csv', mode = 'r') as file:
        csv_file = csv.reader(file, delimiter=',')
        for row in csv_file:
            ingredients.extend(row)
    return ingredients

class Recipe:
    def __init__(self, name, instructions, ingredients, meal_type, vegetarian, prep_time):
        self.name = name
        self.instructions = instructions
        self.ingredients = ingredients
        self.meal_type = meal_type
        self.vegetarian = vegetarian
        self.prep_time = prep_time


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
