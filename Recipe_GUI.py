import Recipe_Logic  # get the extrapolated database
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTableWidget,
    QTableWidgetItem, QDialog, QFormLayout, QTextEdit, QPushButton, QMenu
)
from PySide6.QtGui import QAction

from Recipe_Logic import get_recipes, extract_ingredients


class Recipe_Suggestions(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recipe Suggestion System")
        self.setGeometry(300, 300, 700, 500)

        # Importing all the valid recipes to show student
        self.available_recipe = []
        self.additional_recipe = []
        self.possible, self.partial = Recipe_Logic.match_ingredients(get_recipes(), extract_ingredients("fridge_ingredients.csv"))
        for recipes in self.possible:
            self.available_recipe.append([recipes.name, recipes.prep_time, recipes.meal_type, recipes.vegetarian])
        for recipe in self.partial:
            self.additional_recipe.append([recipe.name, recipe.prep_time, recipe.meal_type, recipe.vegetarian])

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        # Define headers and data
        headers = ["Recipe Name", "Time", "Meal Type", "Veg/Non-Veg"]

        # Available Recipes Table
        layout.addWidget(QLabel("Available Recipes"))
        self.available_recipes_table = QTableWidget()
        self.setup_and_populate_table(self.available_recipes_table, self.available_recipe, headers)
        layout.addWidget(self.available_recipes_table)

        # Additional Recipes Table
        layout.addWidget(QLabel("Additional Recipes"))
        self.additional_recipes_table = QTableWidget()
        self.setup_and_populate_table(self.additional_recipes_table, self.additional_recipe, headers)
        layout.addWidget(self.additional_recipes_table)

        # Connect table click signals to the method that opens the recipe details window
        self.available_recipes_table.cellClicked.connect(self.show_recipe_details)
        self.additional_recipes_table.cellClicked.connect(self.show_recipe_details)

        # Filter Buttons
        self.filter_button1 = QPushButton("Filter Button 1: Choose meal-type", self)
        self.filter_button1.setGeometry(100, 100, 250, 50)
        layout.addWidget(self.filter_button1)

        self.filter_button2 = QPushButton("Filter Button 2: Choose Veg/Non-Veg", self)
        self.filter_button2.setGeometry(100, 200, 250, 50)
        layout.addWidget(self.filter_button2)

        # Create menus for the buttons
        self.menu1 = QMenu(self)
        self.menu2 = QMenu(self)

        # Meal Type Options for Filter Button 1
        self.option_dinner = QAction("Dinner", self)
        self.option_lunch = QAction("Lunch", self)
        self.option_breakfast = QAction("Breakfast", self)
        self.option_show_all1 = QAction("Show All", self)

        self.option_dinner.triggered.connect(self.filter_by_meal_type)
        self.option_lunch.triggered.connect(self.filter_by_meal_type)
        self.option_breakfast.triggered.connect(self.filter_by_meal_type)
        self.option_show_all1.triggered.connect(self.show_all_recipes)

        self.menu1.addAction(self.option_breakfast)
        self.menu1.addAction(self.option_lunch)
        self.menu1.addAction(self.option_dinner)
        self.menu1.addAction(self.option_show_all1)

        # Veg/Non-Veg Options for Filter Button 2
        self.option_veg = QAction("Veg", self)
        self.option_non_veg = QAction("Non-Veg", self)
        self.option_show_all2 = QAction("Show All", self)

        self.option_veg.triggered.connect(self.filter_by_veg_status)
        self.option_non_veg.triggered.connect(self.filter_by_veg_status)
        self.option_show_all2.triggered.connect(self.show_all_recipes)


        self.menu2.addAction(self.option_veg)
        self.menu2.addAction(self.option_non_veg)
        self.menu2.addAction(self.option_show_all2)


        # Connect buttons to show their respective menus
        self.filter_button1.clicked.connect(self.show_menu1)
        self.filter_button2.clicked.connect(self.show_menu2)

    def show_menu1(self):
        # Show the first menu at the filter_button1's position
        self.menu1.exec(self.filter_button1.mapToGlobal(self.filter_button1.rect().bottomLeft()))

    def show_menu2(self):
        # Show the second menu at the filter_button2's position
        self.menu2.exec(self.filter_button2.mapToGlobal(self.filter_button2.rect().bottomLeft()))

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
        table = self.sender()
        recipe_name = table.item(row, 0).text()
        self.details_window = RecipeDetailsWindow(recipe_name)
        self.details_window.setWindowTitle(f"{recipe_name} - Recipe Details")
        self.details_window.show()


    def filter_by_meal_type(self):
        selected_option = self.sender().text()  # Get the text of the selected option

        # Filter the available and additional recipes table  based on meal type
        filtered_available_recipe = [recipe for recipe in self.available_recipe if recipe[2] == selected_option]
        filtered_additional_recipe = [recipe for recipe in self.additional_recipe if recipe[2] == selected_option]

        self.setup_and_populate_table(self.available_recipes_table, filtered_available_recipe,
                                      ["Recipe Name", "Time", "Meal Type", "Veg/Non-Veg"])
        self.setup_and_populate_table(self.additional_recipes_table, filtered_additional_recipe,
                                      ["Recipe Name", "Time", "Meal Type", "Veg/Non-Veg"])


    def filter_by_veg_status(self):
        # Filter the available and additional recipes based on veg/non-veg status

        selected_option = self.sender().text()  # Get the text of the selected option
        if selected_option == "Veg":
            filtered_available_recipe = [recipe for recipe in self.available_recipe if recipe[3] == "Veg"]
            filtered_additional_recipe = [recipe for recipe in self.additional_recipe if recipe[3] == "Veg"]
        else:
            filtered_available_recipe = [recipe for recipe in self.available_recipe if recipe[3] == "Non-Veg"]
            filtered_additional_recipe = [recipe for recipe in self.additional_recipe if recipe[3] == "Non-Veg"]

        self.setup_and_populate_table(self.available_recipes_table, filtered_available_recipe, ["Recipe Name", "Time", "Meal Type", "Veg/Non-Veg"])
        self.setup_and_populate_table(self.additional_recipes_table, filtered_additional_recipe, ["Recipe Name", "Time", "Meal Type", "Veg/Non-Veg"])

    def show_all_recipes(self):
        """Resets the tables ."""
        self.setup_and_populate_table(self.available_recipes_table, self.available_recipe,
                                      ["Recipe Name", "Time", "Meal Type", "Veg/Non-Veg"])
        self.setup_and_populate_table(self.additional_recipes_table, self.additional_recipe,
                                      ["Recipe Name", "Time", "Meal Type", "Veg/Non-Veg"])

class RecipeDetailsWindow(QDialog):
    def __init__(self, recipe_name):
        super().__init__()
        self.setWindowTitle(f"{recipe_name} - Recipe Details")
        self.setGeometry(150, 150, 400, 300)

        # Create layout for the recipe details window
        layout = QFormLayout(self)
        recipes = get_recipes()
        instructions = f"Instructions for {recipe_name}:\n\n"
        for recipe in recipes:
            if recipe.name == recipe_name:
                instructions += recipe.instructions

        self.instructions_text = QTextEdit(self)
        self.instructions_text.setText(instructions)
        self.instructions_text.setReadOnly(True)

        layout.addWidget(QLabel("Recipe Instructions"))
        layout.addWidget(self.instructions_text)

        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.accept)
        layout.addWidget(self.close_button)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Recipe_Suggestions()
    window.show()
    sys.exit(app.exec())
