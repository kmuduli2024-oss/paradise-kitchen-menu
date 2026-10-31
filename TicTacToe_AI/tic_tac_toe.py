import tkinter as tk
from tkinter import messagebox
import random
import json
import os
import time

# ============================================================
#          ADVANCED TIC-TAC-TOE AI
#      MINIMAX + ALPHA-BETA PRUNING
# ============================================================

HUMAN = "X"
AI = "O"
EMPTY = ""

SAVE_FILE = "tic_tac_toe_stats.json"

board = [EMPTY] * 9

current_player = HUMAN
game_mode = "AI"
difficulty = "Hard"

game_over = False

game_start_time = 0
game_end_time = 0
timer_running = False
timer_job = None

move_history = []
redo_history = []

scores = {
    "wins": 0,
    "losses": 0,
    "draws": 0,
    "games": 0,
    "streak": 0
}

buttons = []

status_label = None
score_label = None
history_label = None
ai_info_label = None
timer_label = None


# ============================================================
#                    WINNING COMBINATIONS
# ============================================================

WINNING_COMBINATIONS = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),

    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),

    (0, 4, 8),
    (2, 4, 6)
]


# ============================================================
#                    LOAD STATISTICS
# ============================================================

def load_statistics():

    global scores

    if os.path.exists(SAVE_FILE):

        try:

            with open(SAVE_FILE, "r") as file:
                data = json.load(file)

            for key in scores:

                if key in data:
                    scores[key] = data[key]

        except Exception:
            pass


# ============================================================
#                    SAVE STATISTICS
# ============================================================

def save_statistics():

    try:

        with open(SAVE_FILE, "w") as file:
            json.dump(scores, file, indent=4)

    except Exception:
        pass


# ============================================================
#                    CHECK WINNER
# ============================================================

def check_winner(state):

    for a, b, c in WINNING_COMBINATIONS:

        if (
            state[a] != EMPTY
            and state[a] == state[b]
            and state[b] == state[c]
        ):

            return state[a], (a, b, c)

    if EMPTY not in state:

        return "Draw", None

    return None, None


# ============================================================
#                    AVAILABLE MOVES
# ============================================================

def available_moves(state):

    return [
        i for i in range(9)
        if state[i] == EMPTY
    ]


# ============================================================
#              MINIMAX + ALPHA-BETA PRUNING
# ============================================================

def minimax(state, depth, maximizing, alpha, beta):

    result, _ = check_winner(state)

    if result == AI:
        return 10 - depth

    if result == HUMAN:
        return depth - 10

    if result == "Draw":
        return 0

    # AI MAXIMIZING
    if maximizing:

        best_score = -float("inf")

        for move in available_moves(state):

            state[move] = AI

            score = minimax(
                state,
                depth + 1,
                False,
                alpha,
                beta
            )

            state[move] = EMPTY

            best_score = max(
                best_score,
                score
            )

            alpha = max(
                alpha,
                score
            )

            # Alpha-Beta Pruning
            if beta <= alpha:
                break

        return best_score

    # HUMAN MINIMIZING
    else:

        best_score = float("inf")

        for move in available_moves(state):

            state[move] = HUMAN

            score = minimax(
                state,
                depth + 1,
                True,
                alpha,
                beta
            )

            state[move] = EMPTY

            best_score = min(
                best_score,
                score
            )

            beta = min(
                beta,
                score
            )

            # Alpha-Beta Pruning
            if beta <= alpha:
                break

        return best_score


# ============================================================
#                       BEST MOVE
# ============================================================

def best_move():

    best_score = -float("inf")
    best_moves = []

    for move in available_moves(board):

        board[move] = AI

        score = minimax(
            board,
            0,
            False,
            -float("inf"),
            float("inf")
        )

        board[move] = EMPTY

        if score > best_score:

            best_score = score
            best_moves = [move]

        elif score == best_score:

            best_moves.append(move)

    if best_moves:

        return random.choice(best_moves)

    return None


# ============================================================
#                       EASY AI
# ============================================================

def easy_ai():

    moves = available_moves(board)

    if moves:

        return random.choice(moves)

    return None


# ============================================================
#                      MEDIUM AI
# ============================================================

def medium_ai():

    # 70% intelligent
    # 30% random

    if random.random() < 0.7:

        return best_move()

    return easy_ai()


# ============================================================
#                       HARD AI
# ============================================================

def hard_ai():

    return best_move()


# ============================================================
#                    GET AI MOVE
# ============================================================

def get_ai_move():

    if difficulty == "Easy":

        return easy_ai()

    elif difficulty == "Medium":

        return medium_ai()

    return hard_ai()


# ============================================================
#                     CLEAR SCREEN
# ============================================================

def clear_screen():

    for widget in window.winfo_children():

        widget.destroy()


# ============================================================
#                     CREATE TITLE
# ============================================================

def create_title(parent, text):

    label = tk.Label(
        parent,
        text=text,
        font=("Segoe UI", 25, "bold"),
        bg="#111827",
        fg="#60A5FA"
    )

    label.pack(pady=20)

    return label


# ============================================================
#                       MAIN MENU
# ============================================================

def show_menu():

    global game_over
    global timer_running

    game_over = False

    timer_running = False

    clear_screen()

    create_title(
        window,
        "🎯 TIC-TAC-TOE AI"
    )

    tk.Label(
        window,
        text="Advanced Intelligent Agent",
        font=("Segoe UI", 12),
        bg="#111827",
        fg="#9CA3AF"
    ).pack(pady=(0, 20))

    # --------------------------------------------------------
    # GAME MODE
    # --------------------------------------------------------

    mode_frame = tk.Frame(
        window,
        bg="#1F2937",
        padx=20,
        pady=15
    )

    mode_frame.pack(
        pady=10,
        padx=30,
        fill="x"
    )

    tk.Label(
        mode_frame,
        text="Game Mode",
        font=("Segoe UI", 14, "bold"),
        bg="#1F2937",
        fg="white"
    ).pack()

    mode_var.set("AI")

    tk.Radiobutton(
        mode_frame,
        text="🤖 Play vs AI",
        variable=mode_var,
        value="AI",
        command=mode_changed,
        font=("Segoe UI", 11),
        bg="#1F2937",
        fg="white",
        selectcolor="#374151",
        activebackground="#1F2937",
        activeforeground="white"
    ).pack(pady=5)

    tk.Radiobutton(
        mode_frame,
        text="👥 Two Players",
        variable=mode_var,
        value="2PLAYER",
        command=mode_changed,
        font=("Segoe UI", 11),
        bg="#1F2937",
        fg="white",
        selectcolor="#374151",
        activebackground="#1F2937",
        activeforeground="white"
    ).pack()

    # --------------------------------------------------------
    # DIFFICULTY
    # --------------------------------------------------------

    difficulty_frame = tk.Frame(
        window,
        bg="#1F2937",
        padx=20,
        pady=15
    )

    difficulty_frame.pack(
        pady=10,
        padx=30,
        fill="x"
    )

    tk.Label(
        difficulty_frame,
        text="AI Difficulty",
        font=("Segoe UI", 14, "bold"),
        bg="#1F2937",
        fg="white"
    ).pack()

    difficulty_var.set("Hard")

    tk.Radiobutton(
        difficulty_frame,
        text="🟢 Easy",
        variable=difficulty_var,
        value="Easy",
        font=("Segoe UI", 10),
        bg="#1F2937",
        fg="white",
        selectcolor="#374151",
        activebackground="#1F2937",
        activeforeground="white"
    ).pack()

    tk.Radiobutton(
        difficulty_frame,
        text="🟡 Medium",
        variable=difficulty_var,
        value="Medium",
        font=("Segoe UI", 10),
        bg="#1F2937",
        fg="white",
        selectcolor="#374151",
        activebackground="#1F2937",
        activeforeground="white"
    ).pack()

    tk.Radiobutton(
        difficulty_frame,
        text="🔴 Hard - Minimax",
        variable=difficulty_var,
        value="Hard",
        font=("Segoe UI", 10),
        bg="#1F2937",
        fg="white",
        selectcolor="#374151",
        activebackground="#1F2937",
        activeforeground="white"
    ).pack()

    # --------------------------------------------------------
    # START GAME
    # --------------------------------------------------------

    tk.Button(
        window,
        text="▶ START GAME",
        command=start_game,
        font=("Segoe UI", 13, "bold"),
        bg="#2563EB",
        fg="white",
        activebackground="#1D4ED8",
        activeforeground="white",
        relief="flat",
        padx=30,
        pady=10
    ).pack(pady=15)

    # --------------------------------------------------------
    # STATISTICS
    # --------------------------------------------------------

    tk.Button(
        window,
        text="📊 Statistics",
        command=show_statistics,
        font=("Segoe UI", 11),
        bg="#374151",
        fg="white",
        relief="flat",
        padx=25,
        pady=8
    ).pack(pady=5)

    # --------------------------------------------------------
    # REFRESH SCORE
    # --------------------------------------------------------

    tk.Button(
        window,
        text="♻ Refresh Score",
        command=reset_score,
        font=("Segoe UI", 11),
        bg="#7C3AED",
        fg="white",
        relief="flat",
        padx=25,
        pady=8
    ).pack(pady=5)

    # --------------------------------------------------------
    # EXIT
    # --------------------------------------------------------

    tk.Button(
        window,
        text="❌ Exit",
        command=window.destroy,
        font=("Segoe UI", 11),
        bg="#991B1B",
        fg="white",
        relief="flat",
        padx=25,
        pady=8
    ).pack(pady=5)

    update_menu_info()


# ============================================================
#                   MODE CHANGED
# ============================================================

def mode_changed():

    if mode_var.get() == "2PLAYER":

        difficulty_var.set("Hard")


# ============================================================
#                    MENU INFORMATION
# ============================================================

def update_menu_info():

    tk.Label(
        window,
        text=(
            f"Games: {scores['games']}   "
            f"Wins: {scores['wins']}   "
            f"Losses: {scores['losses']}   "
            f"Draws: {scores['draws']}"
        ),
        font=("Segoe UI", 10),
        bg="#111827",
        fg="#9CA3AF"
    ).pack(pady=15)


# ============================================================
#                      START GAME
# ============================================================

def start_game():

    global game_mode
    global difficulty

    game_mode = mode_var.get()

    difficulty = difficulty_var.get()

    start_new_game()


# ============================================================
#                    START NEW GAME
# ============================================================

def start_new_game():

    global board
    global current_player
    global game_over
    global move_history
    global redo_history
    global game_start_time
    global game_end_time
    global timer_running
    global timer_job

    # Stop old timer

    timer_running = False

    if timer_job is not None:

        try:
            window.after_cancel(timer_job)

        except:
            pass

    # Reset board

    board = [EMPTY] * 9

    current_player = HUMAN

    game_over = False

    move_history = []

    redo_history = []

    # Start timer

    game_start_time = time.time()

    game_end_time = 0

    timer_running = True

    create_game_screen()

    update_board()

    update_status()

    update_timer()


# ============================================================
#                     GAME TIMER
# ============================================================

def update_timer():

    global timer_job

    if not timer_running:

        return

    elapsed = time.time() - game_start_time

    minutes = int(elapsed // 60)

    seconds = int(elapsed % 60)

    timer_label.config(
        text=f"⏱️ Time: {minutes:02d}:{seconds:02d}"
    )

    timer_job = window.after(
        1000,
        update_timer
    )


# ============================================================
#                     GAME SCREEN
# ============================================================

def create_game_screen():

    clear_screen()

    tk.Label(
        window,
        text="🎮 TIC-TAC-TOE",
        font=("Segoe UI", 24, "bold"),
        bg="#111827",
        fg="#60A5FA"
    ).pack(pady=8)

    global status_label

    status_label = tk.Label(
        window,
        text="",
        font=("Segoe UI", 13, "bold"),
        bg="#111827",
        fg="#F9FAFB"
    )

    status_label.pack(pady=3)

    # --------------------------------------------------------
    # TIMER
    # --------------------------------------------------------

    global timer_label

    timer_label = tk.Label(
        window,
        text="⏱️ Time: 00:00",
        font=("Segoe UI", 12, "bold"),
        bg="#111827",
        fg="#FBBF24"
    )

    timer_label.pack(pady=3)

    # --------------------------------------------------------
    # SCORE
    # --------------------------------------------------------

    global score_label

    score_label = tk.Label(
        window,
        text="",
        font=("Segoe UI", 10),
        bg="#111827",
        fg="#9CA3AF"
    )

    score_label.pack(pady=3)

    # --------------------------------------------------------
    # BOARD
    # --------------------------------------------------------

    board_frame = tk.Frame(
        window,
        bg="#111827"
    )

    board_frame.pack(pady=12)

    global buttons

    buttons = []

    for i in range(9):

        button = tk.Button(
            board_frame,
            text="",
            font=("Segoe UI", 28, "bold"),
            width=3,
            height=1,
            bg="#1F2937",
            fg="white",
            activebackground="#374151",
            activeforeground="white",
            relief="flat",
            command=lambda index=i: make_move(index)
        )

        button.grid(
            row=i // 3,
            column=i % 3,
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5
        )

        buttons.append(button)

    # --------------------------------------------------------
    # CONTROLS
    # --------------------------------------------------------

    controls = tk.Frame(
        window,
        bg="#111827"
    )

    controls.pack(pady=8)

    tk.Button(
        controls,
        text="↩ Undo",
        command=undo_move,
        font=("Segoe UI", 10, "bold"),
        bg="#374151",
        fg="white",
        relief="flat",
        padx=12,
        pady=6
    ).grid(
        row=0,
        column=0,
        padx=3
    )

    tk.Button(
        controls,
        text="🔄 Play Again",
        command=start_new_game,
        font=("Segoe UI", 10, "bold"),
        bg="#2563EB",
        fg="white",
        relief="flat",
        padx=12,
        pady=6
    ).grid(
        row=0,
        column=1,
        padx=3
    )

    tk.Button(
        controls,
        text="🏠 Menu",
        command=show_menu,
        font=("Segoe UI", 10, "bold"),
        bg="#374151",
        fg="white",
        relief="flat",
        padx=12,
        pady=6
    ).grid(
        row=0,
        column=2,
        padx=3
    )

    # --------------------------------------------------------
    # RESET GAME
    # --------------------------------------------------------

    tk.Button(
        controls,
        text="🔁 Reset Game",
        command=start_new_game,
        font=("Segoe UI", 10, "bold"),
        bg="#059669",
        fg="white",
        relief="flat",
        padx=12,
        pady=6
    ).grid(
        row=1,
        column=0,
        padx=3,
        pady=6
    )

    # --------------------------------------------------------
    # REFRESH SCORE
    # --------------------------------------------------------

    tk.Button(
        controls,
        text="♻ Refresh Score",
        command=reset_score,
        font=("Segoe UI", 10, "bold"),
        bg="#7C3AED",
        fg="white",
        relief="flat",
        padx=12,
        pady=6
    ).grid(
        row=1,
        column=1,
        padx=3,
        pady=6
    )

    # --------------------------------------------------------
    # EXIT
    # --------------------------------------------------------

    tk.Button(
        controls,
        text="❌ Exit",
        command=window.destroy,
        font=("Segoe UI", 10, "bold"),
        bg="#991B1B",
        fg="white",
        relief="flat",
        padx=12,
        pady=6
    ).grid(
        row=1,
        column=2,
        padx=3,
        pady=6
    )

    # --------------------------------------------------------
    # MOVE HISTORY
    # --------------------------------------------------------

    tk.Label(
        window,
        text="📜 Move History",
        font=("Segoe UI", 11, "bold"),
        bg="#111827",
        fg="#D1D5DB"
    ).pack(pady=(5, 2))

    global history_label

    history_label = tk.Label(
        window,
        text="No moves yet",
        font=("Segoe UI", 9),
        bg="#111827",
        fg="#9CA3AF",
        wraplength=450
    )

    history_label.pack(pady=2)

    # --------------------------------------------------------
    # AI INFORMATION
    # --------------------------------------------------------

    global ai_info_label

    ai_info_label = tk.Label(
        window,
        text="",
        font=("Segoe UI", 9),
        bg="#111827",
        fg="#60A5FA"
    )

    ai_info_label.pack(pady=4)


# ============================================================
#                     HUMAN MOVE
# ============================================================

def make_move(index):

    global current_player

    if game_over:
        return

    if board[index] != EMPTY:
        return

    # Prevent clicking during AI turn

    if game_mode == "AI" and current_player == AI:
        return

    board[index] = current_player

    move_history.append(
        (current_player, index)
    )

    redo_history.clear()

    update_board()

    result = check_game()

    if result:
        return

    # --------------------------------------------------------
    # AI MODE
    # --------------------------------------------------------

    if game_mode == "AI":

        current_player = AI

        update_status()

        window.after(
            400,
            ai_move
        )

    # --------------------------------------------------------
    # TWO PLAYER MODE
    # --------------------------------------------------------

    else:

        if current_player == HUMAN:

            current_player = AI

        else:

            current_player = HUMAN

        update_status()


# ============================================================
#                         AI MOVE
# ============================================================

def ai_move():

    global current_player

    if game_over:
        return

    if game_mode != "AI":
        return

    ai_info_label.config(
        text="🤖 AI is thinking..."
    )

    window.update()

    start = time.time()

    move = get_ai_move()

    thinking_time = time.time() - start

    if move is not None:

        board[move] = AI

        move_history.append(
            (AI, move)
        )

        redo_history.clear()

    ai_info_label.config(
        text=f"🤖 AI decided in {thinking_time:.4f} seconds"
    )

    update_board()

    result = check_game()

    if result:
        return

    current_player = HUMAN

    update_status()


# ============================================================
#                     CHECK GAME
# ============================================================

def check_game():

    global game_over
    global timer_running
    global game_end_time

    winner, winning_cells = check_winner(board)

    if winner is None:

        return False

    # Game finished

    game_over = True

    timer_running = False

    game_end_time = time.time()

    total_time = (
        game_end_time -
        game_start_time
    )

    # Highlight winning cells

    if winning_cells:

        for index in winning_cells:

            buttons[index].config(
                bg="#16A34A",
                fg="white"
            )

    # --------------------------------------------------------
    # AI WINS
    # --------------------------------------------------------

    if winner == AI:

        scores["losses"] += 1

        scores["games"] += 1

        scores["streak"] = 0

        save_statistics()

        show_game_over(
            "🤖 AI Wins!",
            total_time
        )

    # --------------------------------------------------------
    # HUMAN WINS
    # --------------------------------------------------------

    elif winner == HUMAN:

        scores["wins"] += 1

        scores["games"] += 1

        scores["streak"] += 1

        save_statistics()

        show_game_over(
            "🏆 You Win!",
            total_time
        )

    # --------------------------------------------------------
    # DRAW
    # --------------------------------------------------------

    else:

        scores["draws"] += 1

        scores["games"] += 1

        save_statistics()

        show_game_over(
            "🤝 It's a Draw!",
            total_time
        )

    return True


# ============================================================
#                    UPDATE BOARD
# ============================================================

def update_board():

    if not buttons:
        return

    for i in range(9):

        buttons[i].config(
            text=board[i]
        )

        if board[i] == HUMAN:

            buttons[i].config(
                fg="#60A5FA"
            )

        elif board[i] == AI:

            buttons[i].config(
                fg="#F87171"
            )

        else:

            buttons[i].config(
                fg="white"
            )

    update_score_label()

    update_history()


# ============================================================
#                     UPDATE SCORE
# ============================================================

def update_score_label():

    if game_mode == "AI":

        score_label.config(
            text=(
                f"You: {scores['wins']}   |   "
                f"AI: {scores['losses']}   |   "
                f"Draw: {scores['draws']}   |   "
                f"🔥 Streak: {scores['streak']}"
            )
        )

    else:

        score_label.config(
            text=(
                f"Player 1: {scores['wins']}   |   "
                f"Player 2: {scores['losses']}   |   "
                f"Draw: {scores['draws']}"
            )
        )


# ============================================================
#                    MOVE HISTORY
# ============================================================

def update_history():

    if not move_history:

        history_label.config(
            text="No moves yet"
        )

        return

    names = []

    for player, position in move_history:

        row = position // 3 + 1

        col = position % 3 + 1

        names.append(
            f"{player}({row},{col})"
        )

    history_label.config(
        text=" → ".join(names)
    )


# ============================================================
#                    UPDATE STATUS
# ============================================================

def update_status():

    if game_over:
        return

    if game_mode == "AI":

        if current_player == HUMAN:

            status_label.config(
                text="Your Turn ❌"
            )

        else:

            status_label.config(
                text="AI Turn ⭕"
            )

    else:

        if current_player == HUMAN:

            status_label.config(
                text="Player 1 Turn ❌"
            )

        else:

            status_label.config(
                text="Player 2 Turn ⭕"
            )


# ============================================================
#                         UNDO
# ============================================================

def undo_move():

    global current_player

    if game_over:
        return

    if not move_history:
        return

    # --------------------------------------------------------
    # AI MODE
    # --------------------------------------------------------

    if game_mode == "AI":

        # Remove AI move

        if len(move_history) >= 2:

            ai_move_data = move_history.pop()

            human_move_data = move_history.pop()

            redo_history.append(
                ai_move_data
            )

            redo_history.append(
                human_move_data
            )

            board[ai_move_data[1]] = EMPTY

            board[human_move_data[1]] = EMPTY

            current_player = HUMAN

    # --------------------------------------------------------
    # TWO PLAYER MODE
    # --------------------------------------------------------

    else:

        last_move = move_history.pop()

        redo_history.append(
            last_move
        )

        board[last_move[1]] = EMPTY

        if last_move[0] == HUMAN:

            current_player = HUMAN

        else:

            current_player = AI

    update_board()

    update_status()


# ============================================================
#                    GAME OVER WINDOW
# ============================================================

def show_game_over(message, total_time):

    minutes = int(
        total_time // 60
    )

    seconds = total_time % 60

    result_window = tk.Toplevel(window)

    result_window.title(
        "Game Over"
    )

    result_window.geometry(
        "390x480"
    )

    result_window.resizable(
        False,
        False
    )

    result_window.configure(
        bg="#111827"
    )

    tk.Label(
        result_window,
        text=message,
        font=("Segoe UI", 22, "bold"),
        bg="#111827",
        fg="#60A5FA"
    ).pack(pady=25)

    # --------------------------------------------------------
    # COMPLETION TIME
    # --------------------------------------------------------

    tk.Label(
        result_window,
        text=(
            f"⏱️ Game Completed In\n"
            f"{minutes:02d}:{seconds:05.2f}"
        ),
        font=("Segoe UI", 16, "bold"),
        bg="#111827",
        fg="#FBBF24"
    ).pack(pady=10)

    # --------------------------------------------------------
    # STATISTICS
    # --------------------------------------------------------

    tk.Label(
        result_window,
        text=(
            f"Games: {scores['games']}\n"
            f"Wins: {scores['wins']}\n"
            f"Losses: {scores['losses']}\n"
            f"Draws: {scores['draws']}\n"
            f"Win Streak: {scores['streak']}"
        ),
        font=("Segoe UI", 11),
        bg="#111827",
        fg="#D1D5DB"
    ).pack(pady=10)

    # --------------------------------------------------------
    # PLAY AGAIN
    # --------------------------------------------------------

    tk.Button(
        result_window,
        text="🔄 Play Again",
        command=lambda: [
            result_window.destroy(),
            start_new_game()
        ],
        font=("Segoe UI", 11, "bold"),
        bg="#2563EB",
        fg="white",
        relief="flat",
        padx=25,
        pady=8
    ).pack(pady=4)

    # --------------------------------------------------------
    # RESET GAME
    # --------------------------------------------------------

    tk.Button(
        result_window,
        text="🔁 Reset Game",
        command=lambda: [
            result_window.destroy(),
            start_new_game()
        ],
        font=("Segoe UI", 11),
        bg="#059669",
        fg="white",
        relief="flat",
        padx=25,
        pady=8
    ).pack(pady=4)

    # --------------------------------------------------------
    # REFRESH SCORE
    # --------------------------------------------------------

    tk.Button(
        result_window,
        text="♻ Refresh Score",
        command=lambda: [
            result_window.destroy(),
            reset_score()
        ],
        font=("Segoe UI", 11),
        bg="#7C3AED",
        fg="white",
        relief="flat",
        padx=25,
        pady=8
    ).pack(pady=4)

    # --------------------------------------------------------
    # MAIN MENU
    # --------------------------------------------------------

    tk.Button(
        result_window,
        text="🏠 Main Menu",
        command=lambda: [
            result_window.destroy(),
            show_menu()
        ],
        font=("Segoe UI", 11),
        bg="#374151",
        fg="white",
        relief="flat",
        padx=25,
        pady=8
    ).pack(pady=4)


# ============================================================
#                       STATISTICS
# ============================================================

def show_statistics():

    stats_window = tk.Toplevel(window)

    stats_window.title(
        "Statistics"
    )

    stats_window.geometry(
        "400x430"
    )

    stats_window.resizable(
        False,
        False
    )

    stats_window.configure(
        bg="#111827"
    )

    tk.Label(
        stats_window,
        text="📊 GAME STATISTICS",
        font=("Segoe UI", 20, "bold"),
        bg="#111827",
        fg="#60A5FA"
    ).pack(pady=25)

    statistics_text = (
        f"🎮 Total Games      : {scores['games']}\n\n"
        f"🏆 Wins             : {scores['wins']}\n\n"
        f"🤖 Losses           : {scores['losses']}\n\n"
        f"🤝 Draws            : {scores['draws']}\n\n"
        f"🔥 Current Streak   : {scores['streak']}"
    )

    tk.Label(
        stats_window,
        text=statistics_text,
        font=("Segoe UI", 13),
        bg="#111827",
        fg="#D1D5DB",
        justify="left"
    ).pack(pady=15)

    tk.Button(
        stats_window,
        text="Close",
        command=stats_window.destroy,
        font=("Segoe UI", 11),
        bg="#374151",
        fg="white",
        relief="flat",
        padx=30,
        pady=8
    ).pack(pady=20)


# ============================================================
#                     REFRESH SCORE
# ============================================================

def reset_score():

    global scores

    answer = messagebox.askyesno(
        "Refresh Score",
        "Are you sure you want to reset all scores and statistics?"
    )

    if not answer:
        return

    scores = {
        "wins": 0,
        "losses": 0,
        "draws": 0,
        "games": 0,
        "streak": 0
    }

    save_statistics()

    messagebox.showinfo(
        "Score Refreshed",
        "All scores and statistics have been reset."
    )

    if score_label:

        try:
            update_score_label()
        except:
            pass


# ============================================================
#                       MAIN WINDOW
# ============================================================

window = tk.Tk()

window.title(
    "Advanced Tic-Tac-Toe AI"
)

window.geometry(
    "520x720"
)

window.minsize(
    500,
    650
)

window.configure(
    bg="#111827"
)

window.resizable(
    True,
    True
)


# ============================================================
#                       VARIABLES
# ============================================================

mode_var = tk.StringVar(
    value="AI"
)

difficulty_var = tk.StringVar(
    value="Hard"
)


# ============================================================
#                  LOAD SAVED STATISTICS
# ============================================================

load_statistics()


# ============================================================
#                       START APP
# ============================================================

show_menu()

window.mainloop()