import tkinter as tk
from tkinter import messagebox
import heapq

class TicTacToeAI:
    def __init__(self, window):
        self.window = window
        self.window.title("Tic-Tac-Toe AI")
        self.grid = [" "] * 9  # Game board
        self.buttons = []
        self.mode = None
        self.node_counter = 0  # Counter to track nodes visited
        self.counter_label = tk.Label(self.window, text="Nodes Visited: 0")
        self.counter_label.grid(row=3, column=1)

        self.setup_board()
        self.display_board()
        self.setup_strategy_options()
        self.setup_show_moves_button()  # Button to show possible next states

    def setup_strategy_options(self):
        strategy_frame = tk.Frame(self.window)
        strategy_frame.grid(row=0, column=0, rowspan=3, padx=10, pady=10)

        strategies = [
            ("Iterative Deepening", "iterative"),
            ("BFS", "bfs"),
            ("DFS", "dfs"),
            ("Uniform Cost", "uniform")
        ]

        for text, mode in strategies:
            tk.Button(strategy_frame, text=text, command=lambda m=mode: self.set_mode(m)).pack(fill=tk.BOTH, pady=5)

    def setup_board(self):
        board_frame = tk.Frame(self.window)
        board_frame.grid(row=0, column=2, rowspan=3, padx=20, pady=10)

        for idx in range(9):
            btn = tk.Button(board_frame, text=" ", font="Arial 30", width=4, height=2, command=lambda i=idx: self.player_turn(i))
            btn.grid(row=idx // 3, column=idx % 3)
            self.buttons.append(btn)

    def display_board(self):
        for idx, btn in enumerate(self.buttons):
            btn.config(text=self.grid[idx])

    def setup_show_moves_button(self):
        show_moves_button = tk.Button(self.window, text="Show Possible Moves", command=self.show_possible_moves)
        show_moves_button.grid(row=4, column=1, pady=10)

    def set_mode(self, mode):
        self.mode = mode
        messagebox.showinfo("Mode Selected", f"Playing against {mode} strategy.")
        self.reset_game()

    def player_turn(self, idx):
        if self.grid[idx] == " " and self.mode:
            self.grid[idx] = "X"
            self.display_board()
            if self.is_winner("X"):
                messagebox.showinfo("Game Over", "You Win!")
                self.reset_game()
            elif " " not in self.grid:
                messagebox.showinfo("Game Over", "It's a Draw!")
                self.reset_game()
            else:
                self.computer_turn()

    def computer_turn(self):
        self.node_counter = 0  # Reset node counter for each computer turn
        move = getattr(self, f"find_{self.mode}_move", lambda: None)()
        self.counter_label.config(text=f"Nodes Visited: {self.node_counter}")
        if move is not None:
            self.grid[move] = "O"
            self.display_board()
            if self.is_winner("O"):
                messagebox.showinfo("Game Over", "Computer Wins!")
                self.reset_game()
            elif " " not in self.grid:
                messagebox.showinfo("Game Over", "It's a Draw!")
                self.reset_game()

    def show_possible_moves(self):
        possible_moves_window = tk.Toplevel(self.window)
        possible_moves_window.title("Possible Next Game States")

        row, col = 0, 0
        for i in range(9):
            if self.grid[i] == " ":
                next_state = self.grid[:]
                next_state[i] = "O"

                frame = tk.Frame(possible_moves_window, borderwidth=2, relief="groove")
                frame.grid(row=row, column=col, padx=5, pady=5)
                for j in range(9):
                    tk.Button(frame, text=next_state[j], font="Arial 12", width=2, height=1, state="disabled").grid(row=j // 3, column=j % 3)
                
                col += 1
                if col > 2:  # Wrap to the next row if there are more than 3 states in the row
                    col = 0
                    row += 1

    def is_winner(self, player):
        wins = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
        return any(all(self.grid[i] == player for i in combo) for combo in wins)

    # Iterative Deepening
    def find_iterative_move(self):
        depth_limit, best_move = 1, None
        while depth_limit <= 9:
            result = self.depth_limited_search(depth_limit)
            if result is not None:
                best_move = result
            depth_limit += 1
        return best_move

    def depth_limited_search(self, limit):
        best_move, max_score = None, float("-inf")
        for i in range(9):
            if self.grid[i] == " ":
                self.grid[i] = "O"
                score = self.minimax(limit, False)
                self.grid[i] = " "
                if score > max_score:
                    max_score, best_move = score, i
        return best_move

    # BFS
    def find_bfs_move(self):
        queue = [(self.grid[:], 0)]
        best_move, best_score = None, -1
        while queue:
            current_grid, depth = queue.pop(0)
            self.node_counter += 1
            for i in range(9):
                if current_grid[i] == " ":
                    next_grid = current_grid[:]
                    next_grid[i] = "O"
                    if self.is_winner("O"):
                        return i
                    score = self.evaluate("O")
                    if score > best_score:
                        best_score, best_move = score, i
                    queue.append((next_grid, depth + 1))
        return best_move

    # DFS
    def find_dfs_move(self):
        best_move, best_score = None, -1

        def dfs(grid, depth):
            nonlocal best_move, best_score
            self.node_counter += 1
            for i in range(9):
                if grid[i] == " ":
                    next_grid = grid[:]
                    next_grid[i] = "O"
                    if self.is_winner("X"):
                        continue
                    elif " " not in next_grid:
                        continue
                    dfs(next_grid, depth + 1)
                    score = self.evaluate("O")
                    if score > best_score:
                        best_score, best_move = score, i

        dfs(self.grid, 0)
        return best_move

    # Uniform Cost
    def find_uniform_move(self):
        queue = []
        for i in range(9):
            if self.grid[i] == " ":
                self.grid[i] = "O"
                score = self.evaluate("O")
                heapq.heappush(queue, (-score, i))  # Push negative score for max-heap
                self.grid[i] = " "
                self.node_counter += 1
        return heapq.heappop(queue)[1] if queue else None

    def evaluate(self, player):
        if self.is_winner(player):
            return 1
        elif self.is_winner("X"):
            return -1
        return 0

    def minimax(self, depth, maximizing):
        self.node_counter += 1
        if self.is_winner("O"):
            return 1
        elif self.is_winner("X"):
            return -1
        elif " " not in self.grid or depth == 0:
            return 0

        if maximizing:
            max_score = float("-inf")
            for i in range(9):
                if self.grid[i] == " ":
                    self.grid[i] = "O"
                    score = self.minimax(depth - 1, False)
                    self.grid[i] = " "
                    max_score = max(score, max_score)
            return max_score
        else:
            min_score = float("inf")
            for i in range(9):
                if self.grid[i] == " ":
                    self.grid[i] = "X"
                    score = self.minimax(depth - 1, True)
                    self.grid[i] = " "
                    min_score = min(score, min_score)
            return min_score

    def reset_game(self):
        self.grid = [" "] * 9
        self.node_counter = 0
        self.display_board()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeAI(root)
    root.mainloop()
