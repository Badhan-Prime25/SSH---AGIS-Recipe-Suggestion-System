import pytest
from PySide6.QtCore import Qt
from Recipe_GUI import Recipe_Suggestions
from pytestqt.qtbot import QtBot
from Recipe_Logic import *


@pytest.fixture
def app(qtbot: QtBot):
    # used to create and initialize the main window.
    window = Recipe_Suggestions()  # Create an instance of the main window
    qtbot.addWidget(window)
    return window


def test_available_recipes_table(app):
    #Test if the 'Available Recipes' table is populated correctly
    table = app.available_recipes_table  # Correct reference to the table
    assert table.rowCount() == 2  # check 2 rows are present
    assert table.columnCount() == 4  # check 4 columns are present
    assert table.item(0, 0).text() == "Spaghetti Bolognese"  # check first recipe
    assert table.item(1, 0).text() == "Vegetable Stir Fry"  # check second recipe


def test_additional_recipes_table(app):
    """Test if the 'Additional Recipes' table is populated correctly."""
    table = app.additional_recipes_table  # Correct reference to the table
    assert table.rowCount() == 3  # Verify 3 rows are present
    assert table.columnCount() == 4  # Verify 4 columns are present
    assert table.item(0, 0).text() == "Chicken Salad"  # Verify the first recipe
    assert table.item(1, 0).text() == "Mushroom Risotto"  # Verify the second recipe
    assert table.item(2, 0).text() == "Pancakes"  # Verify the third recipe


def test_recipe_details_window(app, qtbot: QtBot):
    """Test if clicking a recipe opens the correct details window."""
    table = app.available_recipes_table  # Reference the 'Available Recipes' table
    recipe_name = table.item(0, 0).text()  # Get the recipe name from the first row

    # Simulate a cell click (row 0, column 0) which emits the signal
    qtbot.mouseClick(table.viewport(), Qt.LeftButton, pos=table.visualRect(table.model().index(0, 0)).center())

    # Use qtbot to wait for the window to appear
    qtbot.waitExposed(app.details_window)

    # Check if the recipe details window opens
    from PySide6.QtWidgets import QApplication
    windows = QApplication.topLevelWidgets()  # Get all top-level widgets
    details_window = next(
        (w for w in windows if w.windowTitle() == f"{recipe_name} - Recipe Details"),
        None,
    )

    # Assert the details window exists
    assert details_window is not None, "Recipe details window did not open."
    assert details_window.instructions_text.toPlainText().startswith("Instructions for Spaghetti Bolognese:")

    # Close the details window
    details_window.close()

@pytest.fixture
def mock_recipes():
    # mock recipes
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
    # mock ingredients
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
    """Test matching available ingredients with recipes."""
    possible, partial = match_ingredients(mock_recipes, mock_ingredients)

    # Fully matched recipe
    assert len(possible) == 1
    assert possible[0].name == "Spaghetti Bolognese"

    # Partially matched recipe
    assert len(partial) == 1
    assert partial[0].name == "Vegetable Stir Fry"
