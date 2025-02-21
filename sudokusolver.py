from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QInputDialog
import sqlite3
import sys

class SudokuSolver(QWidget):
    def __init__(self):
        super().__init__()
        # Initialize database and UI components
        self.init_db()
        self.init_ui()

    def init_db(self):
        """Initialize the SQLite database and create a table for storing puzzles."""
        conn = sqlite3.connect("sudoku.db")
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS puzzles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                grid TEXT
            )
        """)
        conn.commit()
        conn.close()

    def init_ui(self):
        """Set up the user interface, including the 9x9 grid and control buttons."""
        self.setWindowTitle("Sudoku Solver")
        self.grid_layout = QGridLayout()
        self.entries = []

        # Create the 9x9 grid of input fields for the Sudoku puzzle
        for row in range(9):
            row_entries = []
            for col in range(9):
                entry = QLineEdit(self)
                entry.setMaxLength(1)
                entry.setFixedSize(40, 40)
                entry.setStyleSheet(self.get_cell_style(row, col))
                self.grid_layout.addWidget(entry, row, col)
                row_entries.append(entry)
            self.entries.append(row_entries)

        # Set up buttons and connect them to their respective functions
        self.solve_button = QPushButton("Solve")
        self.clear_button = QPushButton("Clear")
        self.save_button = QPushButton("Save Puzzle")
        self.load_button = QPushButton("Load Puzzle")
        self.delete_button = QPushButton("Delete Puzzle")

        self.solve_button.clicked.connect(self.solve)
        self.clear_button.clicked.connect(self.clear_board)
        self.save_button.clicked.connect(self.save_puzzle)
        self.load_button.clicked.connect(self.load_puzzle)
        self.delete_button.clicked.connect(self.delete_puzzle)

        # Arrange buttons in a horizontal layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.solve_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.delete_button)

        # Add grid and button layouts to the main vertical layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.grid_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def get_cell_style(self, row, col):
        """Generate a style string for the cell, adding borders for subgrid boundaries."""
        border_style = "border: 1px solid black;"
        # Add thicker borders for the subgrid boundaries
        if row % 3 == 0:
            border_style += " border-top: 3px solid black;"
        if col % 3 == 0:
            border_style += " border-left: 3px solid black;"
        if row == 8:
            border_style += " border-bottom: 3px solid black;"
        if col == 8:
            border_style += " border-right: 3px solid black;"

        return f"font-size: 18px; text-align: center; {border_style}"

    def save_puzzle(self):
        """Prompt for a puzzle name and save the current puzzle grid to the database."""
        name, ok = self.get_text_input("Save Puzzle", "Enter puzzle name:")
        if not ok or not name:
            return
        grid = "\n".join(" ".join(self.entries[row][col].text() or "0" for col in range(9)) for row in range(9))

        conn = sqlite3.connect("sudoku.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO puzzles (name, grid) VALUES (?, ?)", (name, grid))
            conn.commit()
            QMessageBox.information(self, "Success", "Puzzle saved successfully!")
        except sqlite3.IntegrityError:
            # Handle case where puzzle name already exists
            QMessageBox.warning(self, "Error", "Puzzle name already exists!")
        conn.close()

    def load_puzzle(self):
        """Load a puzzle from the database and display it in the grid."""
        puzzle_name = self.get_puzzle_selection()
        if not puzzle_name:
            return

        conn = sqlite3.connect("sudoku.db")
        c = conn.cursor()
        c.execute("SELECT grid FROM puzzles WHERE name = ?", (puzzle_name,))
        grid_data = c.fetchone()
        conn.close()

        if grid_data:
            grid = grid_data[0].split("\n")
            # Populate the grid with the saved values
            for row in range(9):
                values = grid[row].split()
                for col in range(9):
                    self.entries[row][col].setText(values[col] if values[col] != "0" else "")

    def delete_puzzle(self):
        """Delete a saved puzzle from the database."""
        puzzle_name = self.get_puzzle_selection()
        if not puzzle_name:
            return

        conn = sqlite3.connect("sudoku.db")
        c = conn.cursor()
        c.execute("DELETE FROM puzzles WHERE name = ?", (puzzle_name,))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Success", "Puzzle deleted successfully!")

    def clear_board(self):
        """Clear all entries on the Sudoku grid."""
        for row in self.entries:
            for entry in row:
                entry.clear()

    def solve(self):
        """Solve the Sudoku puzzle if valid, and display the solution in the grid."""
        grid = []
        for row in range(9):
            row_values = []
            for col in range(9):
                value = self.entries[row][col].text()
                row_values.append(int(value) if value.isdigit() else 0)
            grid.append(row_values)

        # Check if the board is valid before attempting to solve
        if not self.is_valid_board(grid):
            QMessageBox.warning(self, "Invalid Board", "This board has no solution.")
            return

        # Attempt to solve the puzzle
        if self.solve_sudoku(grid):
            for row in range(9):
                for col in range(9):
                    self.entries[row][col].setText(str(grid[row][col]))
        else:
            QMessageBox.warning(self, "No Solution", "No solution exists for this Sudoku.")

    def solve_sudoku(self, grid):
        """Recursive backtracking algorithm to solve the Sudoku puzzle."""
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(grid, row, col, num):
                            grid[row][col] = num
                            if self.solve_sudoku(grid):
                                return True
                            grid[row][col] = 0
                    return False
        return True

    def is_valid(self, grid, row, col, num):
        """Check if a number can be placed at the given row and column without
        violating Sudoku rules."""
        for i in range(9):
            if grid[row][i] == num or grid[i][col] == num:
                return False
        box_row, box_col = (row // 3) * 3, (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if grid[box_row + i][box_col + j] == num:
                    return False
        return True

    def is_valid_board(self, grid):
        """Check if the current board is valid (no duplicates in rows or columns)."""
        # Check rows for duplicates
        for row in range(9):
            seen = set()
            for col in range(9):
                value = grid[row][col]
                if value != 0:  # Skip empty cells
                    if value in seen:
                        return False
                    seen.add(value)

        # Check columns for duplicates
        for col in range(9):
            seen = set()
            for row in range(9):
                value = grid[row][col]
                if value != 0:  # Skip empty cells
                    if value in seen:
                        return False
                    seen.add(value)

        return True

    def get_text_input(self, title, message):
        """Prompt the user to input text (used for puzzle names)."""
        text, ok = QInputDialog.getText(self, title, message)
        return text, ok

    def get_puzzle_selection(self):
        """Prompt the user to select a saved puzzle from the database."""
        conn = sqlite3.connect("sudoku.db")
        c = conn.cursor()
        c.execute("SELECT name FROM puzzles")
        puzzles = [row[0] for row in c.fetchall()]
        conn.close()

        if not puzzles:
            QMessageBox.information(self, "No Puzzles", "No saved puzzles found.")
            return None

        puzzle_name, ok = QInputDialog.getItem(self, "Select Puzzle", "Choose a puzzle:", puzzles, 0, False)
        return puzzle_name if ok else None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SudokuSolver()
    window.show()
    sys.exit(app.exec_())
