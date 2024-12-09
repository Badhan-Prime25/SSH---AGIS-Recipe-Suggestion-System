import pytest
from Recipe_Logic import *

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


def test_extract_ingredients(tmp_path):
    # test extract ingredients
    # Create a temporary CSV file
    file_path = tmp_path / "ingredients.csv"
    with open(file_path, "w") as f:
        f.write("Amount,Ingredient\n")
        f.write("100g,pasta\n")
        f.write("200ml,sauce\n")

    ingredients = extract_ingredients(file_path)
    assert ingredients == [["100g", "pasta"], ["200ml", "sauce"]]

def test_match_ingredients(mock_recipes, mock_ingredients):
    #Test matching available ingredients with recipes
    possible, partial = match_ingredients(mock_recipes, mock_ingredients)

    # Fully matched recipe available recipes
    assert len(possible) == 1
    assert possible[0].name == "Spaghetti Bolognese"

    # Partially matched recipe additional recipes
    assert len(partial) == 1
    assert partial[0].name == "Vegetable Stir Fry"