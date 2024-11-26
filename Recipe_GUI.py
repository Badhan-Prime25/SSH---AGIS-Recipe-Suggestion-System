import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTableWidget,
    QTableWidgetItem, QDialog, QFormLayout, QTextEdit, QPushButton
)

class Recipe_Suggestions(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recipe Suggestion System")
        self.setGeometry(300, 300, 700, 500)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Define headers and data
        headers = ["Recipe Name", "Time", "Meal Type", "Veg/Non-Veg"]
        available_recipes = [
            ["White Pasta", "20 Minutes", "Lunch/Dinner", "Non-Veg"],
            ["Pancakes", "10 Minutes", "Breakfast", "Veg"],
            ["Chicken Salad", "30 Minutes", "Dinner", "Non-Veg"],
        ]
        additional_recipes = [
            ["Spaghetti Bolognese", "20 Minutes", "Lunch/Dinner", "Non-Veg"],
            ["Apple Pie", "10 Minutes", "Breakfast", "Veg"],
            ["Chicken Rice", "30 Minutes", "Dinner", "Non-Veg"],
        ]

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

        # Hardcoded recipe instructions
        instructions = f"Instructions for {recipe_name}:\n\n"
        if recipe_name == "White Pasta":
            instructions += "1. Boil water...\n2. Cook pasta...\n3. Prepare sauce...\n4. Mix and serve."
        elif recipe_name == "Pancakes":
            instructions += "1. Mix ingredients...\n2. Heat pan...\n3. Pour batter...\n4. Flip pancakes..."
        elif recipe_name == "Chicken Salad":
            instructions += "1. Chop chicken...\n2. Prepare vegetables...\n3. Toss together..."
        elif recipe_name == "Spaghetti Bolognese":
            instructions += "1. Cook spaghetti...\n2. Prepare meat sauce...\n3. Combine and serve."
        elif recipe_name == "Apple Pie":
            instructions += "1. Prepare the crust...\n2. Mix apples...\n3. Bake and serve."
        elif recipe_name == "Chicken Rice":
            instructions += "1. Cook chicken...\n2. Prepare rice...\n3. Mix and serve."
        else:
            instructions += "Recipe instructions are not available."

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

