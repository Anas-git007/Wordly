import random
import pygame
import requests
from tkinter import *
from tkinter.messagebox import showerror, askretrycancel, askyesno

class WordGame:
    def __init__(self, root):
        self.play_music("music.mp3")
        self.root = root
        frame = Frame(root)
        frame.grid()

        self.target_word = self.fetch_word_from_api()  # Get only valid English words
        print(f"Target Word: {self.target_word}")  # Debugging

        self.entries = []  
        self.match_labels = []  
        self.current_row = 0  

        frame.configure(bg='light blue')
        root.configure(bg='light blue')
        self.label = Label(frame, text="WORDLY", font=('Frijole', 30), justify='center',bg='light blue')
        self.label.grid(row=0, column=0, columnspan=6, pady=10)

        for i in range(4):  
            root.grid_columnconfigure(i, minsize=40)

        for j in range(8):  
            root.grid_rowconfigure(j, minsize=40)

        for row in range(8):
            row_entries = []  
            for col in range(4):
                entry = Entry(frame, font=('Arial', 20), width=2, bd=2, relief='solid', justify='center')
                entry.grid(row=row+1, column=col, padx=5, pady=5)
                for key in range(65,91):
                    entry.bind(f"<KeyRelease-{chr(key)}>", lambda e, r=row, c=col: self.validate_entry(e, r, c))
                    entry.bind(f"<KeyRelease-{chr(key+32)}>", lambda e, r=row, c=col: self.validate_entry(e, r, c))
                entry.bind("<KeyRelease-Right>", lambda e, r=row, c=col: self.validate_entry(e, r, c))
                entry.bind("<KeyRelease-Left>", lambda e, r=row, c=col: self.move_to_previous_widget(e, r, c))
                entry.bind("<KeyRelease-BackSpace>", lambda e, r=row, c=col: self.move_to_previous_widget(e, r, c))

                row_entries.append(entry)
            self.entries.append(row_entries)

            match_label_1 = Label(frame, text="0", font=('Arial', 20), width=4, justify='center', background='yellow', bd=2, relief="solid")
            match_label_1.grid(row=row+1, column=4, padx=5, pady=5)

            match_label_2 = Label(frame, text="0", font=('Arial', 20), width=4, justify='center', background='green', bd=2, relief="solid")
            match_label_2.grid(row=row+1, column=5, padx=5, pady=5)

            self.match_labels.append((match_label_1, match_label_2))
        self.entries[0][0].focus()
        self.submit_btn = Button(frame, text="Submit", font=('Arial', 14), bg="#D8D78F", fg="black", bd=2, relief="groove", state=DISABLED, command=self.submit_row)
        self.submit_btn.grid(row=9, column=2, columnspan=2, pady=10)
        self.root.bind('<Return>', lambda event=None: self.submit_btn.invoke())

    def fetch_word_from_api(self):
        """ Fetch a random valid 4-letter English word from Wordnik API. """
        try:
            url = "https://api.datamuse.com/words?sp=????&max=1000"
            response = requests.get(url)

            if response.status_code == 200:
                words = [word_data['word'].upper() for word_data in response.json()]
                valid_words = [word for word in words if len(set(word)) == len(word)]

                if valid_words:
                    return random.choice(valid_words)
        except Exception as e:
            print("API Error:", e)

        # Fallback in case of API failure
        fallback_words = ["PLAY", "JUMP", "WAVE", "QUIZ", "FISH"]
        return random.choice(fallback_words)

    def is_valid_word(self, word):
        """ Check if the word is a valid English word using Wordnik API. """
        try:
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word.lower()}"
            response = requests.get(url)
            return response.status_code == 200
        except:
            return False  

    def play_music(self,music):
        self.music=music
        pygame.mixer.init()
        try:
            pygame.mixer.music.load(music)  
            pygame.mixer.music.play()
        except:
            print("Music file not found!")

    def validate_entry(self, event, row, col):
        """ Validate input: only allow uppercase letters """
        if row != self.current_row:
            return  

        entry = self.entries[row][col]
        value = entry.get()

        if value.isalpha() and len(value) == 1:
            entry.delete(0, END)
            entry.insert(0, value.upper())  
        elif len(value) > 1:
            entry.delete(1, END)  

        self.focus_next_widget(row, col)
        self.check_row_completion(row)

    def move_to_previous_widget(self, event, row, col):
        """ Move cursor to previous entry if backspace is pressed """
        entry = self.entries[row][col]
        if col > 0 and entry.get() == "":
            self.entries[row][col - 1].focus()
        
    def focus_next_widget(self, row, col):
        """ Moves to the next entry widget """
        if col < 3:
            self.entries[row][col + 1].focus()

    def check_row_completion(self, row):
        """ Enable submit button if row is fully filled """
        if all(self.entries[row][col].get() for col in range(4)):
            self.submit_btn.config(state=NORMAL)
        else:
            self.submit_btn.config(state=DISABLED)

    def submit_row(self):
        """ Handles submission of a row """
        guessed_word = "".join(self.entries[self.current_row][col].get().upper() for col in range(4))

        if not self.is_valid_word(guessed_word):
            showerror("Invalid Word", f"{guessed_word} is not a valid word!")
            return  

        if guessed_word == self.target_word:
            self.play_music("confetti.mp3")
            if askyesno("Congratulations!", "Congratulations! You guessed the word!\nDo you want to continue playing?"):
                self.root.destroy()
                StartNewGame()
            self.root.destroy()  

        self.update_match_labels(guessed_word)
        self.submit_btn.config(state=DISABLED)  

        if self.current_row < 7:
            self.current_row += 1
            self.entries[self.current_row][0].focus()
        else:
            # All rows are filled, ask if the user wants to play again
            self.play_music("fail.mp3")
            if askretrycancel("Game Over", "Game Over\nAlas! Do you want to Retry?"):
                self.root.destroy()  # Close the current game
                StartNewGame()  # Start a new game
            else:
                self.root.destroy()  # Exit the game

    def update_match_labels(self, guessed_word):
        """ Updates labels based on letter positions """
        target_chars = list(self.target_word)
        guessed_chars = list(guessed_word)
        match_label_1, match_label_2 = self.match_labels[self.current_row]

        correct_count = sum(1 for i in range(4) if guessed_chars[i] == target_chars[i])
        misplaced_count = sum(1 for i in range(4) if guessed_chars[i] in target_chars and guessed_chars[i] != target_chars[i])

        match_label_1.config(text=f"{misplaced_count}")
        match_label_2.config(text=f"{correct_count}")

class StartNewGame:
    def __init__(self):
        new_root = Tk()
        new_root.title("WORDLY!")
        new_root.geometry("345x530+100+100")
        WordGame(new_root)
        new_root.mainloop()

root = Tk()
root.title("WORDLY!")
root.geometry("345x530+100+100")
WordGame(root)
root.mainloop()
