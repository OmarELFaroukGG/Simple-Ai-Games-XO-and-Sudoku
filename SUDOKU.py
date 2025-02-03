#Name: Omar El Farouk Ahmed Ahmed - 320220146 - CNC - section 2
import random
import copy

def valid_move(board, r, c, n):
    """Check if placing a number in board[r][c] follows Sudoku rules."""
    if n in board[r] or n in [board[i][c] for i in range(9)]:
        return False
    sr, sc = 3 * (r // 3), 3 * (c // 3)
    return all(n != board[i][j] for i in range(sr, sr + 3) for j in range(sc, sc + 3))

def sudoku_solver(board):
    """Backtracking algorithm to solve Sudoku."""
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                for n in random.sample(range(1, 10), 9):  # Randomized numbers
                    if valid_move(board, r, c, n):
                        board[r][c] = n
                        if sudoku_solver(board):
                            return True
                        board[r][c] = 0
                return False
    return True

def complete_sudoku():
    """Generate a complete valid Sudoku board."""
    grid = [[0] * 9 for _ in range(9)]
    sudoku_solver(grid)  # Fill the grid using solver
    return grid

def create_puzzle(grid, blanks=40):
    """Remove numbers from a full grid to create a Sudoku puzzle."""
    puzzle = copy.deepcopy(grid)
    for r, c in random.sample([(i, j) for i in range(9) for j in range(9)], blanks):
        puzzle[r][c] = 0
    return puzzle

def display_board(board):
    """Display the Sudoku board in a readable format."""
    for row in board:
        print(" ".join(str(n) if n != 0 else "." for n in row))

def main():
    # Generate and display a complete Sudoku grid
    full_grid = complete_sudoku()
    print("Complete Sudoku Grid:")
    display_board(full_grid)

    # Create a puzzle by removing numbers
    puzzle = create_puzzle(full_grid)
    print("\nSudoku Puzzle:")
    display_board(puzzle)

    # Solve the puzzle and display the result
    solution = copy.deepcopy(puzzle)
    if sudoku_solver(solution):
        print("\nSolved Sudoku Grid:")
        display_board(solution)
    else:
        print("\nNo solution exists for the puzzle.")

if __name__ == "__main__":
    main()
