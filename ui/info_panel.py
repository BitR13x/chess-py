"""UI components for the chess game"""

import tkinter as tk
from tkinter import scrolledtext


class InfoPanel:
    def __init__(self, parent: tk.Frame):
        self.frame = tk.Frame(parent)
        self.frame.pack(
            side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10
        )

        # Score display
        self.score_label = tk.Label(
            self.frame,
            text="Score\n\nWhite: 0\nBlack: 0",
            font=("Arial", 14),
            justify=tk.LEFT,
        )
        self.score_label.pack(pady=10)

        # Move history
        tk.Label(
            self.frame, text="Move History", font=("Arial", 12, "bold")
        ).pack()
        self.move_history_frame = tk.Frame(self.frame)
        self.move_history_frame.pack(fill=tk.BOTH, expand=True)

        self.move_history_scrollbar = tk.Scrollbar(self.move_history_frame)
        self.move_history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.move_history_text = tk.Text(
            self.move_history_frame,
            width=20,
            height=20,
            yscrollcommand=self.move_history_scrollbar.set,
        )
        self.move_history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.move_history_scrollbar.config(
            command=self.move_history_text.yview
        )

    def update_score(self, white_score: int, black_score: int) -> None:
        """Update the score display"""
        self.score_label.config(
            text=f"Score\n\nWhite: {white_score}\nBlack: {black_score}"
        )

    def add_move(
        self, move_notation: str, move_number: int, is_white: bool
    ) -> None:
        """Add a move to the history display"""
        if is_white:
            self.move_history_text.insert(
                tk.END, f"{move_number}. {move_notation} "
            )
        else:
            self.move_history_text.insert(tk.END, f"{move_notation}\n")
        self.move_history_text.see(tk.END)

    def clear_history(self) -> None:
        """Clear the move history display"""
        self.move_history_text.delete("1.0", tk.END)

    def rebuild_history(self, move_history: list) -> None:
        """Rebuild the entire move history display"""
        self.clear_history()
        for i, move in enumerate(move_history):
            move_num = (i + 1) // 2 + ((i + 1) % 2)
            if i % 2 == 0:
                self.move_history_text.insert(
                    tk.END, f"{move_num}. {move['notation']} "
                )
            else:
                self.move_history_text.insert(tk.END, f"{move['notation']}\n")


class ControlPanel:
    def __init__(self, parent: tk.Frame, callbacks: dict):
        self.frame = tk.Frame(parent)
        self.frame.pack(pady=10)

        tk.Button(self.frame, text="Undo", command=callbacks["undo"]).pack(
            fill=tk.X, pady=2
        )
        tk.Button(
            self.frame, text="Flip Board", command=callbacks["flip"]
        ).pack(fill=tk.X, pady=2)
        tk.Button(
            self.frame, text="Save Game", command=callbacks["save"]
        ).pack(fill=tk.X, pady=2)
        tk.Button(
            self.frame, text="Load Game", command=callbacks["load"]
        ).pack(fill=tk.X, pady=2)
        tk.Button(
            self.frame, text="New Game", command=callbacks["new_game"]
        ).pack(fill=tk.X, pady=2)
