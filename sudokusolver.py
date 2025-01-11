import tkinter as tk
from tkinter import messagebox

# Function to check if placing num in grid[row][col] is valid
def is_valid(grid, row, col, num):
    # Check if the number is in the current row
    for i in range(9):
        if grid[row][i] == num:
            return False

    # Check if the number is in the current column
    for i in range(9):
        if grid[i][col] == num:
            return False

    # Check if the number is in the current 3x3 grid
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] == num:
                return False

    return True

# Function to solve the Sudoku using backtracking
def solve_sudoku(grid):
    # Find the next empty cell
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:  # 0 indicates an empty cell
                # Try numbers from 1 to 9
                for num in range(1, 10):
                    if is_valid(grid, row, col, num):
                        # Place the number
                        grid[row][col] = num
                        # Recursively solve the next cell
                        if solve_sudoku(grid):
                            return True
                        # If it doesn't work, backtrack (reset the cell)
                        grid[row][col] = 0
                return False  # If no number works, backtrack
    return True  # If the entire grid is filled

# Function to handle the solving process when the user presses the "Solve" button
def solve():
    # Convert the entries into a 2D list (grid)
    grid = []
    for row in range(9):
        row_values = []
        for col in range(9):
            try:
                value = int(entries[row][col].get())
                if value < 0 or value > 9:
                    raise ValueError
                row_values.append(value)
            except ValueError:
                row_values.append(0)  # Empty cells will be represented by 0
        grid.append(row_values)

    # Solve the Sudoku
    if solve_sudoku(grid):
        # Update the grid with the solution
        for row in range(9):
            for col in range(9):
                entries[row][col].delete(0, tk.END)
                entries[row][col].insert(tk.END, str(grid[row][col]))
    else:
        messagebox.showerror("No Solution", "No solution exists for this Sudoku.")

# Function to create the Sudoku grid interface
def create_gui():
    global entries
    entries = []
    window = tk.Tk()
    window.title("Sudoku Solver")

    # Create the 9x9 grid of entry boxes
    for row in range(9):
        row_entries = []
        for col in range(9):
            entry = tk.Entry(window, width=5, font=("Arial", 18), justify="center", bd=2, relief="solid")
            entry.grid(row=row, column=col, padx=5, pady=5)
            row_entries.append(entry)
        entries.append(row_entries)

    # Add a solve button
    solve_button = tk.Button(window, text="Solve", font=("Arial", 14), command=solve)
    solve_button.grid(row=9, column=0, columnspan=9, pady=10)

    window.mainloop()

# Run the GUI
create_gui()
