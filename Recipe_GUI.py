import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTableWidget,
    QTableWidgetItem, QDialog, QFormLayout, QTextEdit, QPushButton
)


class Recipe_Suggestions(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recipe Suggestion System")
        self.setGeometry(100, 100, 600, 400)
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        # Available Recipes Table
        layout.addWidget(QLabel("Available Recipes"))
        self.available_recipes_table = QTableWidget()
        self.setup_table(self.available_recipes_table)
        layout.addWidget(self.available_recipes_table)
        # only usign hardcoded data initially then going to change it to actual db data
        available_recipes = [
            ["White Pasta", "20 Minutes", "Lunch/Dinner", "Non-Veg"],
            ["Pancakes", "10 Minutes", "Breakfast", "Veg"],
            ["Chicken Salad", "30 Minutes", "Dinner", "Non-Veg"],
        ]
        self.populate_table_(self.available_recipes_table, available_recipes)
        # Additional Recipes Table
        layout.addWidget(QLabel("Additional Recipes"))
        self.additional_recipes_table = QTableWidget()
        self.setup_table(self.additional_recipes_table)
        layout.addWidget(self.additional_recipes_table)
        # hardcoded data for an example
        additional_recipes = [
            ["Spaghetti Bolognese", "20 Minutes", "Lunch/Dinner", "Non-Veg"],
            ["Apple Pie", "10 Minutes", "Breakfast", "Veg"],
            ["Chicken Rice", "30 Minutes", "Dinner", "Non-Veg"],
        ]
        self.populate_table_(self.additional_recipes_table, additional_recipes)
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
        # example hardcoded instructions nneed to change later
        instructions = f"Instructions for {recipe_name}:\n\n"
        if recipe_name == "White Pasta":
            instructions += "1. Boil water\n2. Cook pasta\n3. Prepare sauce\n4. Mix and serve."
        elif recipe_name == "Pancakes":
            instructions += "1. Mix ingredients\n2. Heat pan\n3. Pour batter.\n4. Flip pancakes."
        elif recipe_name == "Chicken Salad":
            instructions += "1. Chop chicken.\n2. Prepare vegetables.\n3. Toss together."
        elif recipe_name == "Spaghetti ":
            instructions += "1. Cook spaghetti.\n2. Prepare meat sauce.\n3. Combine and serve."
        elif recipe_name == "Apple Pie":
            instructions += "1. Prepare the crust.\n2. Mix apples.\n3. Bake and serve."
        elif recipe_name == "Chicken Rice":
            instructions += "1. Cook chicken.\n2. Prepare rice.\n3. Mix and serve."
        # new window to show recipe instructions from the databas
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
