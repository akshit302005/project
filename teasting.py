import random
import tkinter as tk
from tkinter import messagebox

class HangmanSetup:
    def __init__(self, master):
        self.master = master
        self.master.title("Hangman Setup")
        self.master.geometry("400x200")

        self.label = tk.Label(self.master, text="Select Difficulty Level:", font=("Helvetica", 14))
        self.label.pack()

        self.difficulty = tk.StringVar()
        self.difficulty.set("Easy")

        self.easy_button = tk.Radiobutton(self.master, text="Easy", variable=self.difficulty, value="Easy", font=("Helvetica", 12))
        self.easy_button.pack()

        self.medium_button = tk.Radiobutton(self.master, text="Medium", variable=self.difficulty, value="Medium", font=("Helvetica", 12))
        self.medium_button.pack()

        self.hard_button = tk.Radiobutton(self.master, text="Hard", variable=self.difficulty, value="Hard", font=("Helvetica", 12))
        self.hard_button.pack()

        self.start_button = tk.Button(self.master, text="Start Game", command=self.start_game, font=("Helvetica", 14))
        self.start_button.pack()

    def start_game(self):
        difficulty_level = self.difficulty.get()
        self.master.destroy()
        root = tk.Tk()
        app = HangmanGame(root, difficulty_level)
        root.mainloop()

class HangmanGame:
    def __init__(self, master, difficulty):
        self.master = master
        self.master.title("Hangman Game")
        self.difficulty = difficulty
        self.word = ""
        self.guessed_letters = []
        self.attempts = 6

        self.canvas = tk.Canvas(self.master, width=400, height=400)
        self.canvas.pack()

        self.word_label = tk.Label(self.master, text="", font=("Helvetica", 24))
        self.word_label.pack()

        self.input_label = tk.Label(self.master, text="Enter a letter:", font=("Helvetica", 14))
        self.input_label.pack()

        self.input_entry = tk.Entry(self.master, font=("Helvetica", 14))
        self.input_entry.pack()

        self.submit_button = tk.Button(self.master, text="Submit", command=self.check_letter, font=("Helvetica", 14))
        self.submit_button.pack()

        self.keyboard_frame = tk.Frame(self.master)
        self.keyboard_frame.pack()

        self.create_keyboard()

        self.try_again_button = tk.Button(self.master, text="Try Again", command=self.try_again, font=("Helvetica", 14))
        self.try_again_button.pack()
        self.try_again_button.pack_forget()

        self.levels = ["Easy", "Medium", "Hard"]
        self.current_level = self.levels.index(difficulty)

        self.choose_word()

    def choose_word(self):
        if self.current_level == 0:  # Easy
            words = ["apple", "banana", "orange", "grape", "kiwi"]
        elif self.current_level == 1:  # Medium
            words = ["watermelon", "pineapple", "strawberry", "blueberry", "peach"]
        elif self.current_level == 2:  # Hard
            words = ["raspberry", "blackberry", "cherry", "apricot", "pomegranate"]
        else:
            words = ["apple", "banana", "orange", "grape", "watermelon", "pineapple", "strawberry"]
        self.word = random.choice(words)

    def display_word(self):
        displayed_word = ""
        for letter in self.word:
            if letter in self.guessed_letters:
                displayed_word += letter
            else:
                displayed_word += "_"
        return displayed_word

    def draw_gallows(self):
        self.canvas.create_line(50, 350, 250, 350)
        self.canvas.create_line(150, 350, 150, 50)
        self.canvas.create_line(150, 50, 250, 50)
        self.canvas.create_line(250, 50, 250, 100)

    def draw_body_parts(self):
        if self.attempts == 5:
            self.canvas.create_oval(230, 100, 270, 140, width=2)
        elif self.attempts == 4:
            self.canvas.create_line(250, 140, 250, 250, width=2)
        elif self.attempts == 3:
            self.canvas.create_line(250, 150, 230, 200, width=2)
        elif self.attempts == 2:
            self.canvas.create_line(250, 150, 270, 200, width=2)
        elif self.attempts == 1:
            self.canvas.create_line(250, 250, 230, 300, width=2)
        elif self.attempts == 0:
            self.canvas.create_line(250, 250, 270, 300, width=2)

    def create_keyboard(self):
        keys = "abcdefghijklmnopqrstuvwxyz"
        for key in keys:
            button = tk.Button(self.keyboard_frame, text=key.upper(), width=4, height=2,
                               command=lambda k=key: self.keyboard_click(k), font=("Helvetica", 10))
            button.grid(row=(ord(key) - 97) // 6, column=(ord(key) - 97) % 6)

    def keyboard_click(self, letter):
        self.input_entry.insert(tk.END, letter.lower())

    def check_letter(self):
        guess = self.input_entry.get().lower()

        if guess in self.guessed_letters:
            messagebox.showinfo("Hangman", "You already guessed that letter!")
            self.input_entry.delete(0, tk.END)
            return
        elif len(guess) != 1 or not guess.isalpha():
            messagebox.showinfo("Hangman", "Please enter a single letter.")
            self.input_entry.delete(0, tk.END)
            return

        self.guessed_letters.append(guess)

        if guess not in self.word:
            self.attempts -= 1
            messagebox.showinfo("Hangman", f"Incorrect! You have {self.attempts} attempts left.")
            self.draw_body_parts()
            if self.attempts == 0:
                messagebox.showinfo("Hangman", f"Sorry, you ran out of attempts! The word was: {self.word}")
                self.end_game()
                return
        else:
            messagebox.showinfo("Hangman", "Correct!")

        self.word_label.config(text=self.display_word())
        self.input_entry.delete(0, tk.END)

        if "_" not in self.display_word():
            if self.current_level < len(self.levels) - 1:
                messagebox.showinfo("Hangman", "Congratulations, you cleared this level!")
                self.current_level += 1
                self.try_again_button.pack()
            else:
                messagebox.showinfo("Hangman", "Congratulations, you completed all levels!")
                self.end_game()
            return

    def try_again(self):
        self.master.destroy()
        root = tk.Tk()
        app = HangmanGame(root, self.levels[self.current_level])
        root.mainloop()

    def end_game(self):
        self.master.destroy()
def main():
    root = tk.Tk()
    app = HangmanSetup(root)
    root.mainloop()

if __name__ == "__main__":
    main()

