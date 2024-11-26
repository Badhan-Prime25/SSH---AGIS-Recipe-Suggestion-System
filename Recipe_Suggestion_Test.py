import pytest
from PySide6.QtCore import Qt
from Recipe_GUI import Recipe_Suggestions  # Ensure the file containing the GUI is named `Recipe_GUI.py`
from pytestqt.qtbot import QtBot


@pytest.fixture
def app(qtbot: QtBot):
    #Fixture to create and initialize the main window.
    window = Recipe_Suggestions()  # Create an instance of the main window
    qtbot.addWidget(window)
    return window


def test_available_recipes_table(app): # this works
    #Test if the 'Available Recipes' table is populated correctly.
    table = app.available_recipes_table  # Correct reference to the table
    assert table.rowCount() == 3  # Verify 3 rows are present
    assert table.columnCount() == 4  # Verify 4 columns are present
    assert table.item(0, 0).text() == "White Pasta"  # Verify the first recipe name


def test_additional_recipes_table(app): # this works
    """Test if the 'Additional Recipes' table is populated correctly."""
    table = app.additional_recipes_table  # Correct reference to the table
    assert table.rowCount() == 3  # Verify 3 rows are present
    assert table.columnCount() == 4  # Verify 4 columns are present
    assert table.item(1, 0).text() == "Apple Pie"  # Verify the second recipe name


def test_recipe_details_window(app, qtbot: QtBot):
    """Test if clicking a recipe opens the correct details window."""
    table = app.available_recipes_table  # Reference the 'Available Recipes' table
    recipe_name = table.item(0, 0).text()  # Get the recipe name from the first row

    # Call show_recipe_details with the table explicitly
    app.show_recipe_details(0, 0, table)  # Pass the table directly

    # Use qtbot to wait for the window to appear
    qtbot.waitExposed(app.details_window)  # Wait until the details window is visible

    # Check if the recipe details window opens
    from PySide6.QtWidgets import QApplication
    windows = QApplication.topLevelWidgets()  # Get all top-level widgets
    details_window = next(
        (w for w in windows if w.windowTitle() == f"{recipe_name} - Recipe Details"),
        None,
    )


    assert details_window is not None, "Recipe details window did not open."
    assert details_window.instructions_text.toPlainText().startswith("Instructions for White Pasta:")

    # Close the details window
    details_window.close()


