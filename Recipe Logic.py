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
