import tkinter as tk
from tkinter import messagebox
import random


class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Game")
        self.root.geometry("400x300")

        self.label = tk.Label(
            self.root, text="Choose a number between 25 and 40:")
        self.label.pack(pady=10)

        self.entry = tk.Entry(self.root)
        self.entry.pack(pady=5)

        self.start_button = tk.Button(
            self.root, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=5)

        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack(pady=10)

        self.player_points_label = tk.Label(self.root, text="Player Points: 0")
        self.player_points_label.pack()
        self.computer_points_label = tk.Label(
            self.root, text="Computer Points: 0")
        self.computer_points_label.pack()
        self.bank_label = tk.Label(self.root, text="Bank: 0")
        self.bank_label.pack()

        self.reset_button = tk.Button(
            self.root, text="Play Again", command=self.reset_game, state="disabled")
        self.reset_button.pack(pady=5)

    def start_game(self):
        try:
            self.target_number = int(self.entry.get())
            if self.target_number < 25 or self.target_number > 40:
                messagebox.showerror(
                    "Error", "Choose a number between 25 and 40")
                return
            self.current_number = 1
            self.computer_points = 0
            self.player_points = 0
            self.bank = 0
            self.update_points_ui()
            self.play_game()
            self.start_button.config(state="disabled")
            self.entry.config(state="disabled")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")

    def update_points_ui(self):
        self.player_points_label.config(
            text=f"Player Points: {self.player_points}")
        self.computer_points_label.config(
            text=f"Computer Points: {self.computer_points}")
        self.bank_label.config(text=f"Bank: {self.bank}")

    def play_game(self):
        while self.current_number < 5000:
            if self.current_number % 2 == 0:
                self.computer_turn()
            else:
                self.player_turn()
            self.update_points_ui()
            self.current_number += 1

        if self.player_points > self.computer_points:
            self.result_label.config(text="You win!")
        elif self.computer_points > self.player_points:
            self.result_label.config(text="Computer wins!")
        else:
            self.result_label.config(text="Tie!")

        self.reset_button.config(state="normal")

    def player_turn(self):
        multiplier = random.choice([2, 3, 4])
        self.current_number *= multiplier
        if self.current_number % 2 == 0:
            self.player_points -= 1
        else:
            self.player_points += 1

        if self.current_number % 10 == 0 or self.current_number % 10 == 5:
            self.bank += 1

    def computer_turn(self):
        best_move = self.minimax(self.current_number, True)
        self.current_number = best_move[0]
        if best_move[1] % 2 == 0:
            self.computer_points -= 1
        else:
            self.computer_points += 1

        if best_move[1] % 10 == 0 or best_move[1] % 10 == 5:
            self.bank += 1

    def minimax(self, number, is_maximizing):
        if number >= 5000:
            return [number, 0]

        if is_maximizing:
            best_value = float('-inf')
            best_move = None
            for multiplier in [2, 3, 4]:
                new_number = number * multiplier
                value = self.minimax(new_number, False)[1]
                if value > best_value:
                    best_value = value
                    best_move = new_number
            return [best_move, best_value]
        else:
            best_value = float('inf')
            best_move = None
            for multiplier in [2, 3, 4]:
                new_number = number * multiplier
                value = self.minimax(new_number, True)[1]
                if value < best_value:
                    best_value = value
                    best_move = new_number
            return [best_move, best_value]

    def reset_game(self):
        self.entry.delete(0, tk.END)
        self.result_label.config(text="")
        self.start_button.config(state="normal")
        self.entry.config(state="normal")
        self.reset_button.config(state="disabled")
        self.player_points = 0
        self.computer_points = 0
        self.bank = 0
        self.update_points_ui()


if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
