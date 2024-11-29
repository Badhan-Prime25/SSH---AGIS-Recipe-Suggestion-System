

import Recipe_Logic # get the extrapolated database
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTableWidget,
    QTableWidgetItem, QDialog, QFormLayout, QTextEdit, QPushButton
)

from Recipe_Logic import get_recipes, extract_ingredients


class Recipe_Suggestions(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recipe Suggestion System")
        self.setGeometry(300, 300, 700, 500)

        # Importing all the valid recipes to show student
        available_recipe = []
        additional_recipe = []
        possible, partial = Recipe_Logic.match_ingredients(get_recipes(), extract_ingredients("fridge_ingredients.csv"))
        for recipes in possible:
            available_recipe.append([recipes.name,recipes.prep_time,recipes.meal_type,recipes.vegetarian])
        for recipe in partial:
            additional_recipe.append([recipe.name,recipe.prep_time,recipe.meal_type,recipe.vegetarian])

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        # Define headers and data
        headers = ["Recipe Name", "Time", "Meal Type", "Veg/Non-Veg"]
        available_recipes = available_recipe
        additional_recipes = additional_recipe

        # Available Recipes Table
        layout.addWidget(QLabel("Available Recipes"))
        self.available_recipes_table = QTableWidget()
        self.setup_and_populate_table(self.available_recipes_table, available_recipes, headers)
        layout.addWidget(self.available_recipes_table)

        # Additional Recipes Table
        layout.addWidget(QLabel("Additional Recipes"))
        self.additional_recipes_table = QTableWidget()
        self.setup_and_populate_table(self.additional_recipes_table, additional_recipes, headers)
        layout.addWidget(self.additional_recipes_table)

        # Connect table click signals to the method that opens the recipe details window
        self.available_recipes_table.cellClicked.connect(self.show_recipe_details)
        self.additional_recipes_table.cellClicked.connect(self.show_recipe_details)

    def setup_and_populate_table(self, table, data, headers):
        """Configures and populates a table with the given data and headers."""
        # Configure the table
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setDefaultSectionSize(120)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)
        table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Populate the table
        table.setRowCount(len(data))
        for row, recipe in enumerate(data):
            for col, value in enumerate(recipe):
                table.setItem(row, col, QTableWidgetItem(str(value)))

    def show_recipe_details(self, row, col):
        """Opens a new window showing recipe details when a recipe is clicked."""
        # Determine the sender table and fetch the recipe name
        table = self.sender()
        recipe_name = table.item(row, 0).text()

        # Instantiate and show the details window
        self.details_window = RecipeDetailsWindow(recipe_name)
        self.details_window.setWindowTitle(f"{recipe_name} - Recipe Details")
        self.details_window.show()


class RecipeDetailsWindow(QDialog):
    def __init__(self, recipe_name):
        super().__init__()
        self.setWindowTitle(f"{recipe_name} - Recipe Details")
        self.setGeometry(150, 150, 400, 300)

        # Create layout for the recipe details window
        layout = QFormLayout(self)
        recipes = get_recipes()
        # Hardcoded recipe instructions
        instructions = f"Instructions for {recipe_name}:\n\n"
        for recipe in recipes:
            if recipe.name == recipe_name:
                instructions += recipe.instructions


        # Create a QTextEdit for displaying the recipe instructions
        self.instructions_text = QTextEdit(self)
        self.instructions_text.setText(instructions)
        self.instructions_text.setReadOnly(True)

        layout.addWidget(QLabel("Recipe Instructions"))
        layout.addWidget(self.instructions_text)

        # Add a close button
        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.accept)
        layout.addWidget(self.close_button)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Recipe_Suggestions()
    window.show()
    sys.exit(app.exec())

