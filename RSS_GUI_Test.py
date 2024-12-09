import pytest
from PySide6.QtCore import Qt
from Recipe_GUI import Recipe_Suggestions
from pytestqt.qtbot import QtBot

@pytest.fixture
def app(qtbot: QtBot):
    #inititalising main window
    window = Recipe_Suggestions()  # simulating main window
    qtbot.addWidget(window)
    return window

def test_available_recipes_table(app): #
    #test what is in available recipes table database data now
    table = app.available_recipes_table
    assert table.rowCount() == 2  # check it has 3 rows
    assert table.columnCount() == 4  # check it has 4 columns
    assert table.item(0, 0).text() == "Spaghetti Bolognese"  #check first recipe database
    assert table.item(1, 0).text() == "Vegetable Stir Fry"  # second recipe

def test_additional_recipes_table(app): #
    #test additional recipes hardcoded data
    table = app.additional_recipes_table
    assert table.rowCount() == 3  # check 3 rows
    assert table.columnCount() == 4  # check 4 columns
    assert table.item(0, 0).text() == "Chicken Salad"  # first recipe
    assert table.item(1, 0).text() == "Mushroom Risotto"  # second recipe
    assert table.item(2, 0).text() == "Pancakes"  # third recipe database recipes

def test_recipe_details_window(app, qtbot: QtBot):

    table = app.available_recipes_table  # Reference the 'Available Recipes' table
    recipe_name = table.item(0, 0).text()  #get first row recipe of database data

    # Simulate clicking on the first recipe of database data
    qtbot.mouseClick(table.viewport(), Qt.LeftButton, pos=table.visualRect(table.model().index(0, 0)).center())

    # wait for the window
    qtbot.waitExposed(app.details_window)

    # Check if the recipe details window opens
    from PySide6.QtWidgets import QApplication
    windows = QApplication.topLevelWidgets()
    details_window = next(
        (w for w in windows if w.windowTitle() == f"{recipe_name} - Recipe Details"),
        None,
    )


    assert details_window is not None, "Recipe details window did not open."
    assert details_window.instructions_text.toPlainText().startswith("Instructions for Spaghetti Bolognese:") # first instruction of database data

    # Close the details window
    details_window.close()