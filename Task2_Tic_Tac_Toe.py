import tkinter as tk
import math
from tkinter import messagebox

# Global board
board = [' ' for _ in range(9)]
buttons = []

# Colors
BG_COLOR = "#2c3e50"
BTN_BG = "#34495e"
BTN_FG = "#ecf0f1"
HOVER_BG = "#1abc9c"
FONT = ("Helvetica", 24, "bold")
WIN_COLOR = "#e74c3c"

# Check win
def is_winner(brd, player):
    win_patterns = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    for pattern in win_patterns:
        if all(brd[i] == player for i in pattern):
            return pattern
    return False

# Check draw
def is_draw(brd):
    return ' ' not in brd

# Get available moves
def get_available_moves(brd):
    return [i for i, spot in enumerate(brd) if spot == ' ']

# Minimax with alpha-beta pruning
def minimax(brd, depth, is_max, alpha, beta):
    if is_winner(brd, 'O'):
        return 10 - depth
    if is_winner(brd, 'X'):
        return depth - 10
    if is_draw(brd):
        return 0

    if is_max:
        best = -math.inf
        for move in get_available_moves(brd):
            brd[move] = 'O'
            score = minimax(brd, depth+1, False, alpha, beta)
            brd[move] = ' '
            best = max(best, score)
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best
    else:
        best = math.inf
        for move in get_available_moves(brd):
            brd[move] = 'X'
            score = minimax(brd, depth+1, True, alpha, beta)
            brd[move] = ' '
            best = min(best, score)
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best

# AI move
def ai_move():
    best_score = -math.inf
    best_move = None
    for move in get_available_moves(board):
        board[move] = 'O'
        score = minimax(board, 0, False, -math.inf, math.inf)
        board[move] = ' '
        if score > best_score:
            best_score = score
            best_move = move
    board[best_move] = 'O'
    buttons[best_move].config(text='O', state='disabled', bg=BTN_BG)
    check_game()

# On player click
def handle_click(i):
    if board[i] == ' ':
        board[i] = 'X'
        buttons[i].config(text='X', state='disabled', bg=BTN_BG)
        check_game()
        if not is_winner(board, 'X') and not is_draw(board):
            root.after(400, ai_move)

# Check result
def check_game():
    x_win = is_winner(board, 'X')
    o_win = is_winner(board, 'O')

    if x_win:
        for i in x_win:
            buttons[i].config(bg=WIN_COLOR)
        messagebox.showinfo("Game Over", "You win!")
        disable_all()
    elif o_win:
        for i in o_win:
            buttons[i].config(bg=WIN_COLOR)
        messagebox.showinfo("Game Over", "AI wins!")
        disable_all()
    elif is_draw(board):
        messagebox.showinfo("Game Over", "It's a draw!")
        disable_all()

# Disable all buttons
def disable_all():
    for btn in buttons:
        btn.config(state='disabled')

# Restart game
def restart_game():
    global board
    board = [' ' for _ in range(9)]
    for i in range(9):
        buttons[i].config(text=' ', state='normal', bg=BTN_BG)

# Hover effect
def on_enter(e):
    btn = e.widget
    idx = buttons.index(btn)
    if board[idx] == ' ':
        btn.config(bg=HOVER_BG)

def on_leave(e):
    btn = e.widget
    idx = buttons.index(btn)
    if board[idx] == ' ':
        btn.config(bg=BTN_BG)

# GUI setup
root = tk.Tk()
root.title("Tic-Tac-Toe AI")
root.configure(bg=BG_COLOR)

# Create buttons
for i in range(9):
    btn = tk.Button(root, text=' ', font=FONT, width=6, height=2, bg=BTN_BG, fg=BTN_FG,
                    activebackground=HOVER_BG, command=lambda i=i: handle_click(i))
    btn.grid(row=i//3, column=i%3, padx=5, pady=5)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    buttons.append(btn)

# Restart button
restart = tk.Button(root, text="Restart", font=("Arial", 14), bg=HOVER_BG, fg="white", command=restart_game)
restart.grid(row=3, column=0, columnspan=3, pady=10)

# Start GUI loop
root.mainloop()
