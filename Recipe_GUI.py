import sys
import Recipe_Logic
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTableWidget,
    QTableWidgetItem, QDialog, QFormLayout, QTextEdit, QPushButton
)

from Recipe_Logic import get_recipes, extract_ingredients


class Recipe_Suggestions(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recipe Suggestion System")
        self.setGeometry(100, 100, 600, 400)

        # Importing all the valid recipes to show the students
        available_recipe = []
        additional_recipe = []
        possible,partial = Recipe_Logic.match_ingredients(get_recipes(),extract_ingredients("fridge_ingredients.csv"))
        for recipe in possible:
            available_recipe.append([recipe.name,recipe.prep_time,recipe.meal_type,recipe.vegetarian])
        for recipes in partial:
            additional_recipe.append([recipes.name, recipes.prep_time, recipes.meal_type, recipes.vegetarian])

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        # Available Recipes Table
        layout.addWidget(QLabel("Available Recipes"))
        self.available_recipes_table = QTableWidget()
        self.setup_table(self.available_recipes_table)
        layout.addWidget(self.available_recipes_table)

        self.populate_table_(self.available_recipes_table, available_recipe)
        # Additional Recipes Table
        layout.addWidget(QLabel("Additional Recipes"))
        self.additional_recipes_table = QTableWidget()
        self.setup_table(self.additional_recipes_table)
        layout.addWidget(self.additional_recipes_table)


        self.populate_table_(self.additional_recipes_table, additional_recipe)
        # open recipe details window
        self.available_recipes_table.cellClicked.connect(self.show_recipe_details)
        self.additional_recipes_table.cellClicked.connect(self.show_recipe_details)


    def setup_table(self, table):
        table.setColumnCount(4)  #4 columns
        table.setHorizontalHeaderLabels(["Recipe Name", "Time", "Meal Type", "Veg/Non-Veg"]) # table titles
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setDefaultSectionSize(120)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)
        table.setEditTriggers(QTableWidget.NoEditTriggers)


    def populate_table_(self, table, data):

        table.setRowCount(len(data))
        for row, recipe in enumerate(data):
            for col, value in enumerate(recipe):
                table.setItem(row, col, QTableWidgetItem(str(value)))


    def show_recipe_details(self, row, col):
        recipe_name = self.sender().item(row, 0).text()
        self.details_window = RecipeDetailsWindow(recipe_name)
        self.details_window.show()


class RecipeDetailsWindow(QDialog):
    def __init__(self, recipe_name):
        super().__init__()
        self.setWindowTitle(f"{recipe_name} - Recipe Details")
        self.setGeometry(150, 150, 400, 300)

        layout = QFormLayout(self)
        recipes = get_recipes() # gets the recipes that match the ingredients you have
        instructions = f"Instructions for {recipe_name}:\n\n"
        for recipe in recipes:
            if recipe.name == recipe_name:
                instructions += recipe.instructions # puts all the instructions into a new webpage

        # new window to show recipe instructions from the database
        self.instructions_text = QTextEdit(self)
        self.instructions_text.setText(instructions)
        self.instructions_text.setReadOnly(True)
        layout.addWidget(QLabel("Recipe Instructions"))
        layout.addWidget(self.instructions_text)
        # closing the window
        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.accept)
        layout.addWidget(self.close_button)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Recipe_Suggestions()
    window.show()
    sys.exit(app.exec())
