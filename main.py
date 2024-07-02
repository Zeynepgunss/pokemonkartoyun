import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

class Pokemon:
    def __init__(self, name="Bilinmeyen Pokemon", damage=0, image_path=""):
        self.__name = name
        self.__damage = damage
        self.__image_path = image_path
        self.__image = ImageTk.PhotoImage(Image.open(image_path).resize((100, 100)))

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_damage(self):
        return self.__damage

    def set_damage(self, damage):
        self.__damage = damage

    def get_image(self):
        return self.__image

    def set_image(self, image_path):
        self.__image_path = image_path
        self.__image = ImageTk.PhotoImage(Image.open(image_path).resize((100, 100)))

    def __str__(self):
        return f"{self.__name} (Hasar: {self.__damage})"

class Player:
    def __init__(self, name="Bilinmeyen Oyuncu"):
        self.__name = name
        self.__hand = []
        self.__score = 0

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_hand(self):
        return self.__hand

    def set_hand(self, hand):
        self.__hand = hand

    def get_score(self):
        return self.__score

    def set_score(self, score):
        self.__score = score

    def draw_card(self, deck):
        if deck:
            self.__hand.append(deck.pop(random.randint(0, len(deck) - 1)))

    def play_card(self, index):
        return self.__hand.pop(index)

    def add_score(self, points):
        self.__score += points

class ComputerPlayer(Player):
    def __init__(self, name="Bilinmeyen Bilgisayar"):
        super().__init__(name)

    def play_card(self, index=None):
        return super().play_card(random.randint(0, len(self.get_hand()) - 1))

class Game:
    def __init__(self, root):
        self.root = root
        self.mode = None
        self.deck = [
            Pokemon("Pikachu", 55, "pikachu.png"),
            Pokemon("Charizard", 85, "charizard.png"),
            Pokemon("Bulbasaur", 49, "bulbasaur.png"),
            Pokemon("Squirtle", 44, "squirtle.png"),
            Pokemon("Jigglypuff", 45, "jigglypuff.png"),
            Pokemon("Gengar", 65, "gengar.png"),
            Pokemon("Eevee", 52, "eevee.png"),
            Pokemon("Snorlax", 110, "snorlax.png"),
            Pokemon("Mewtwo", 90, "mewtwo.png"),
            Pokemon("Dragonite", 95, "dragonite.png")
        ]
        self.player1 = None
        self.player2 = None
        self.setup_mode_selection()

    def setup_mode_selection(self):
        mode_frame = tk.Frame(self.root)
        mode_frame.pack(pady=20)

        mode_label = tk.Label(mode_frame, text="Oyun Modunu Seçiniz:")
        mode_label.pack()

        player_vs_computer_btn = tk.Button(mode_frame, text="Oyuncu vs Bilgisayar", command=lambda: self.start_game("player_vs_computer"))
        player_vs_computer_btn.pack(pady=10)

        computer_vs_computer_btn = tk.Button(mode_frame, text="Bilgisayar vs Bilgisayar", command=lambda: self.start_game("computer_vs_computer"))
        computer_vs_computer_btn.pack(pady=10)

    def start_game(self, mode):
        self.mode = mode
        for widget in self.root.winfo_children():
            widget.destroy()

        if self.mode == "player_vs_computer":
            self.player1 = Player("Oyuncu (1)")
            self.player2 = ComputerPlayer("Bilgisayar")
            self.setup_game()
            self.create_widgets()
        elif self.mode == "computer_vs_computer":
            self.player1 = ComputerPlayer("Bilgisayar (1)")
            self.player2 = ComputerPlayer("Bilgisayar (2)")
            self.setup_game()
            self.create_widgets()

        self.update_ui()

    def setup_game(self):
        for _ in range(3):
            self.player1.draw_card(self.deck)
            self.player2.draw_card(self.deck)
        self.table = [self.deck.pop() for _ in range(4)]
        self.player_card = None
        self.computer_card = None

    def create_widgets(self):
        try:
            self.player1_frame = tk.Frame(self.root)
            self.player1_frame.pack(pady=10)

            self.player1_label = tk.Label(self.player1_frame, text=f"{self.player1.get_name()} Kartları:")
            self.player1_label.pack()

            self.player1_buttons = []
            for i, card in enumerate(self.player1.get_hand()):
                btn = tk.Button(self.player1_frame, text=str(card), image=card.get_image(), compound=tk.TOP, command=lambda i=i: self.player_turn(i))
                btn.pack(side=tk.LEFT, padx=5)
                self.player1_buttons.append(btn)

            self.table_frame = tk.Frame(self.root)
            self.table_frame.pack(pady=10)

            self.table_label = tk.Label(self.table_frame, text="Ortadaki Kartlar:")
            self.table_label.pack()

            self.table_player_label = tk.Label(self.table_frame, text="Kapalı")
            self.table_player_label.pack(side=tk.LEFT, padx=5)

            self.table_computer_label = tk.Label(self.table_frame, text="Kapalı")
            self.table_computer_label.pack(side=tk.LEFT, padx=5)

            self.computer_frame = tk.Frame(self.root)
            self.computer_frame.pack(pady=10)

            self.computer_label = tk.Label(self.computer_frame, text=f"{self.player2.get_name()} Kartları:")
            self.computer_label.pack()

            self.computer_buttons = []
            for i, card in enumerate(self.player2.get_hand()):
                btn = tk.Button(self.computer_frame, text=str(card), image=card.get_image(), compound=tk.TOP, state=tk.DISABLED)
                btn.pack(side=tk.LEFT, padx=5)
                self.computer_buttons.append(btn)

            self.play_button = tk.Button(self.root, text="Aç", state=tk.DISABLED, command=self.reveal_cards)
            self.play_button.pack(pady=10)

            self.score_label = tk.Label(self.root, text=f"Skor: {self.player1.get_name()} 0 - 0 {self.player2.get_name()}")
            self.score_label.pack(pady=10)
        except tk._tkinter.TclError:
            pass

    def update_ui(self):
        try:
            for i, card in enumerate(self.player1.get_hand()):
                self.player1_buttons[i].config(text=str(card), image=card.get_image(), compound=tk.TOP, state=tk.NORMAL)

            for i in range(len(self.player1.get_hand()), 3):
                self.player1_buttons[i].config(text="Boş", state=tk.DISABLED)

            for i, card in enumerate(self.player2.get_hand()):
                self.computer_buttons[i].config(text=str(card), image=card.get_image(), compound=tk.TOP)

            for i in range(len(self.player2.get_hand()), 3):
                self.computer_buttons[i].config(text="Boş", state=tk.DISABLED)

            self.score_label.config(
                text=f"Skor: {self.player1.get_name()} {self.player1.get_score()} - {self.player2.get_score()} {self.player2.get_name()}")

            self.table_player_label.config(text="Kapalı" if not self.player_card else self.player_card.get_name())
            self.table_computer_label.config(text="Kapalı" if not self.computer_card else self.computer_card.get_name())

            if not self.player1.get_hand() and not self.deck:
                self.end_game()
        except tk._tkinter.TclError:
            pass

    def player_turn(self, card_index):
        try:
            self.player_card = self.player1.play_card(card_index)
            self.computer_card = self.player2.play_card()
            self.play_button.config(state=tk.NORMAL)
            for btn in self.player1_buttons:
                btn.config(state=tk.DISABLED)
        except tk._tkinter.TclError:
            pass

    def reveal_cards(self):
        result = f"{self.player1.get_name()} oynadı: {self.player_card}\n{self.player2.get_name()} oynadı: {self.computer_card}\n"

        if self.player_card.get_damage() > self.computer_card.get_damage():
            result += f"{self.player1.get_name()} turu kazandı!"
            self.player1.add_score(5)
        elif self.computer_card.get_damage() > self.player_card.get_damage():
            result += f"{self.player2.get_name()} turu kazandı!"
            self.player2.add_score(5)
        else:
            result += "Bu tur berabere!"

        messagebox.showinfo("Tur Sonucu", result)

        if self.table:
            self.player1.draw_card(self.table)
            self.player2.draw_card(self.table)

        self.player_card = None
        self.computer_card = None
        self.play_button.config(state=tk.DISABLED)
        self.update_ui()

        if not self.player1.get_hand() and not self.deck:
            self.end_game()

    def end_game(self):
        if self.player1.get_score() > self.player2.get_score():
            result = f"{self.player1.get_name()} kazandı! Skor: {self.player1.get_score()} - {self.player2.get_score()}"
        elif self.player2.get_score() > self.player1.get_score():
            result = f"{self.player2.get_name()} kazandı! Skor: {self.player2.get_score()} - {self.player1.get_score()}"
        else:
            result = f"Oyun berabere! Skor: {self.player1.get_score()} - {self.player2.get_score()}"

        messagebox.showinfo("Oyun Bitti", result)
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pokemon Kart Oyunu - Mod Seçimi")
    game = Game(root)
    root.mainloop()


