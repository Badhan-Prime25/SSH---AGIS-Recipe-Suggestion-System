import pytest
from Recipe_Logic import *
import sqlite3




@pytest.fixture(scope="module")
def actual_db():
    # connecting to our food database
    connection = sqlite3.connect("foodDatabase.db")
    cursor = connection.cursor()
    yield cursor  # cursor used for testing
    connection.close()  # Closing connection after tests to stop db from being altered


# test get_recipes using test database

@pytest.fixture
def mock_recipes():
    # mock recipes we use for testing
    return [
        Recipe("Spaghetti Bolognese", "Cook pasta. Add sauce.",
               [["100g", "pasta"], ["200ml", "sauce"]],
               "Lunch/Dinner", 30, 0),
        Recipe("Vegetable Stir Fry", "Chop vegetables. Stir fry.",
               [["1", "carrot"], ["1", "broccoli"], ["2 tbsp", "soy sauce"]],
               "Lunch/Dinner", 20, 1),
    ]

@pytest.fixture
def mock_ingredients():
    # mock ingredients we use for testing
    return [
        ["150g", "pasta"],
        ["300ml", "sauce"],
        ["1", "carrot"],
        ["1", "broccoli"],
        ["1 tbsp", "soy sauce"],


    ]
def test_split_ingredient():
    #Test the split_ingredient function.
    assert split_ingredient("1 tbsp olive oil") == ["1 tbsp", "olive oil"]
    assert split_ingredient("100g pasta") == ["100g", "pasta"]
    assert split_ingredient("salt") == ["salt", ""]


def test_extract_ingredients():
    # test extract ingredients
    file_path = "fridge_ingredients.csv" # path to our fridge ingredients
    ingredients = extract_ingredients(file_path)

    expected_ingredients = [
        ["1 breast", "Chicken Breast"],
        ["1 cup", "Carrots"],
        ["1 cup", "Flour"],
        ["1 cup", "Rice"],
        ["1 cup", "Tomato Sauce"],
        ["1 tbsp", "Chili Powder"],
        ["1 tbsp", "Garlic Paste"],
        ["1 tbsp", "Lemon Juice"],
        ["1 cup", "Mixed Greens"],
        ["1 tbsp", "Mustard"],
        ["1 tsp", "Black Pepper"],
        ["1 tsp", "Ginger Paste"],
        ["1 tsp", "Salt"],
        ["100g", "Sugar"],
        ["100g", "Tomatoes"],
        ["2", "Eggs"],
        ["2 cups", "Baby Spinach"],
        ["2 cups", "Mixed Greens"],
        ["2 tbsp", "Mayonnaise"],
        ["2 tbsp", "Olive Oil"],
        ["2 tbsp", "Vinegar"],
        ["200g", "Chicken Thighs"],
        ["200g", "Mushrooms"],
        ["200g", "Potatoes"],
        ["200g", "Spaghetti"],
        ["250ml", "Milk"],
        ["3 tbsp", "Butter"],
        ["3 tbsp", "Soy Sauce"],
        ["500g", "Ground Beef"],
        ["50g", "Basil Leaves"],
    ]

    # if they dont match
    assert ingredients == expected_ingredients, "Extracted ingredients do not match the expected output."

def test_match_ingredients(mock_recipes, mock_ingredients):
    #Test matching available ingredients with recipes
    possible, partial = match_ingredients(mock_recipes, mock_ingredients)

    # Fully matched recipe / available recipes
    assert len(possible) == 1
    assert possible[0].name == "Spaghetti Bolognese"

    # Partially matched recipe / additional recipes
    assert len(partial) == 1
    assert partial[0].name == "Vegetable Stir Fry"

def test_get_recipes_actual_db(actual_db):
    global repCur
    repCur = actual_db # cursor points to our food db

    recipes = get_recipes() # we use get recipes to get data from our food db


    assert len(recipes) > 0, "No recipes found in the database" # we check at least onne recipes

    # loop through our recipes
    for recipe in recipes:
        assert recipe.name, "Recipe name is missing" # check get_recipes retrieved the name
        assert recipe.instructions, "Recipe instructions are missing" # check get_recipes retrieved the instructions
        assert recipe.ingredients, "Recipe ingredients are missing" #check get_recipes retrieved the ingredients
        assert isinstance(recipe.ingredients, list), "Ingredients should be a list of lists" # check get_recipes ingredients is a list
        assert recipe.meal_type, "Meal type is missing" # check get_recipes retrieved the meal type

