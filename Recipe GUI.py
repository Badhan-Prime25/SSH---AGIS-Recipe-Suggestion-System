class Recipe:
    def __init__(self, name, ingredients, instructions, meal_type, veg_status, prep_time):
        self.name = name
        self.ingredients = ingredients  # list of ingredients in the recipe
        self.instructions = instructions  # list of instructions
        self.meal_type = meal_type  # string telling you what type of meal this is
        self.veg_status = veg_status  # bool flag showing whether recipe is vegan or not
        self.prep_time = prep_time  # int telling you how long the recipe will take to make in minutes


def match_ingredients(ingredients, recipes):
    ingredients_list = ingredients.split(',')