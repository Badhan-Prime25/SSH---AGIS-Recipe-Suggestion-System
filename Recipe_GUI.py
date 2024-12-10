import sys
import Recipe_Logic
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTableWidget,
    QTableWidgetItem, QDialog, QFormLayout, QTextEdit, QPushButton,QMenu
)
from PySide6.QtGui import QAction

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

        # variables for the filter buttons
        self.available_recipe = available_recipe
        self.additional_recipe = additional_recipe
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


        # Filter Buttons
        self.filter_button1 = QPushButton("Filter Button 1: Choose meal-type", self)
        self.filter_button1.setGeometry(100, 100, 250, 50)
        layout.addWidget(self.filter_button1)

        self.filter_button2 = QPushButton("Filter Button 2: Choose Veg/Non-Veg", self)
        self.filter_button2.setGeometry(100, 200, 250, 50)
        layout.addWidget(self.filter_button2)

        # Creating the  menus for the buttons
        self.menu1 = QMenu(self)
        self.menu2 = QMenu(self)

        # Options for meal type filter Button
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

        # Options for Veg/Non-Veg  filter Button
        self.option_veg = QAction("Veg", self)
        self.option_non_veg = QAction("Non-Veg", self)
        self.option_show_all2 = QAction("Show All", self)

        self.option_veg.triggered.connect(self.filter_by_veg_status)
        self.option_non_veg.triggered.connect(self.filter_by_veg_status)
        self.option_show_all2.triggered.connect(self.show_all_recipes)


        self.menu2.addAction(self.option_veg)
        self.menu2.addAction(self.option_non_veg)
        self.menu2.addAction(self.option_show_all2)


        # Connecting the buttons to show their respective menus
        self.filter_button1.clicked.connect(self.show_menu1)
        self.filter_button2.clicked.connect(self.show_menu2)

    # Showing the  menus
    def show_menu1(self):
        self.menu1.exec(self.filter_button1.mapToGlobal(self.filter_button1.rect().bottomLeft()))

    def show_menu2(self):
        self.menu2.exec(self.filter_button2.mapToGlobal(self.filter_button2.rect().bottomLeft()))

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

#Functions to filter recipes

        # Filtering the available and additional recipes tables  based on meal type
    def filter_by_meal_type(self):
        selected_option = self.sender().text()
        filtered_available_recipe = [recipe for recipe in self.available_recipe if recipe[2] == selected_option]
        filtered_additional_recipe = [recipe for recipe in self.additional_recipe if recipe[2] == selected_option]

        self.populate_table_(self.available_recipes_table, filtered_available_recipe)
        self.populate_table_(self.additional_recipes_table, filtered_additional_recipe)

    # Filtering the available and additional recipes tables based on veg/non-veg status
    def filter_by_veg_status(self):
        selected_option = self.sender().text()
        if selected_option == "Veg":
            filtered_available_recipe = [recipe for recipe in self.available_recipe if recipe[3] == "Veg"]
            filtered_additional_recipe = [recipe for recipe in self.additional_recipe if recipe[3] == "Veg"]
        else:
            filtered_available_recipe = [recipe for recipe in self.available_recipe if recipe[3] == "Non-Veg"]
            filtered_additional_recipe = [recipe for recipe in self.additional_recipe if recipe[3] == "Non-Veg"]

        self.populate_table_(self.available_recipes_table, filtered_available_recipe)
        self.populate_table_(self.additional_recipes_table, filtered_additional_recipe)

#Resetting the tables to their original data
    def show_all_recipes(self):
        self.populate_table_(self.additional_recipes_table, self.additional_recipe)
        self.populate_table_(self.available_recipes_table, self.available_recipe)


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
