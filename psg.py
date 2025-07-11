import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont
import json
import os
from PIL import Image, ImageTk

class ScoreboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PSG ScoreBoard")
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Configure>", self.resize_fonts)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=1)

        self.base_font = tkFont.Font(family="Arial", size=8)
        self.label_font = tkFont.Font(family="Arial", size=9, weight="bold")

        self.teams = [
            "The Killers (JP/Teo)", "Foo Fighters (Sam/Ecap)",
            "Arctic Monkeys (Jack/Blango)", "Greenday (Isaiah/Jake)",
            "Coldplay (Mello/Kells)", "All American Rejects (HL/Zdog)",
            "Fallout Boys (Jesse/OD)"
        ]
        self.games = [
            "Volleyball", "Toe Jam", "Knocker Ball", "Pickle Ball",
            "Treasure Hunt", "Watering Hole", "ChipShot", "3 Point Contest",
            "Dodgeball", "Gauntlet"
        ]

        self.score_entries = []
        self.scores = {team: [0] * len(self.games) for team in self.teams}
        self.totalScore = {team: 0 for team in self.teams}

        self.load_scores()
        self.create_ui()

    def create_ui(self):
        self.game_frame = tk.Frame(self.root)
        self.game_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        for i in range(len(self.games) + 1):
            self.game_frame.grid_rowconfigure(i, weight=1)
        for j in range(len(self.teams) + 1):
            self.game_frame.grid_columnconfigure(j, weight=1)

        for col, team in enumerate(self.teams):
            team_label = tk.Label(self.game_frame, text=team, font=self.base_font, relief="solid")
            team_label.grid(row=0, column=col + 1, padx=2, pady=3, sticky="nsew")

        self.create_game_slots()

        update_button = tk.Button(self.root, text="Update Scores", font=self.label_font, command=self.update_scores)
        update_button.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        self.total_score_frame = tk.Frame(self.root)
        self.total_score_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.total_score_frame.grid_columnconfigure(0, weight=1)
        self.total_score_frame.grid_columnconfigure(1, weight=3)
        self.total_score_frame.grid_columnconfigure(2, weight=2)

        title_label = tk.Label(self.total_score_frame, text="Total Scores", font=self.label_font)
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky="nsew")

        self.total_score_labels = {}
        for i in range(len(self.teams)):
            place_label = tk.Label(self.total_score_frame, text=f"{i+1}:", font=self.label_font)
            place_label.grid(row=i + 1, column=0, padx=2, pady=3, sticky="nsew")

            team_label = tk.Label(self.total_score_frame, text="", font=self.base_font, relief="solid")
            team_label.grid(row=i + 1, column=1, padx=2, pady=3, sticky="nsew")

            score_label = tk.Label(self.total_score_frame, text="", font=self.base_font, relief="solid")
            score_label.grid(row=i + 1, column=2, padx=2, pady=3, sticky="nsew")

            self.total_score_labels[f"team_{i}"] = team_label
            self.total_score_labels[f"score_{i}"] = score_label

        tournament_points = ["10", "8", "6", "5", "4", "3", "2"]
        round_robin_points = ["10", "8", "6", "5", "4", "3", "2"]

        tk.Label(self.total_score_frame, text="\nRound Robin Pointing:", font=self.label_font).grid(row=10, column=0, columnspan=3, sticky="w")
        for i in range(7):
            text = f"Place {i+1}: {tournament_points[i]}"
            tk.Label(self.total_score_frame, text=text, font=self.base_font).grid(row=11+i, column=0, columnspan=3, sticky="w")

        tk.Label(self.total_score_frame, text="\nTournament Pointing:", font=self.label_font).grid(row=18, column=0, columnspan=3, sticky="w")
        for i in range(7):
            text = f"Place {i+1}: {round_robin_points[i]}"
            tk.Label(self.total_score_frame, text=text, font=self.base_font).grid(row=19+i, column=0, columnspan=3, sticky="w")

        # Load and display the bracket image
        image_path = "bracket1.png"  # Ensure bracket.png is in the same folder
        pil_image = Image.open(image_path).resize((400, 399))  # Resize as needed
        self.tk_image = ImageTk.PhotoImage(pil_image)

        # Place image in UI (e.g., row 27 in total_score_frame)
        image_label = tk.Label(self.total_score_frame, image=self.tk_image)
        image_label.grid(row=26, column=0, columnspan=3, pady=3, sticky="w")
        self.display_scores()

    def create_game_slots(self):
        for i, game in enumerate(self.games):
            game_label = tk.Label(self.game_frame, text=game, font=self.base_font, relief="solid")
            game_label.grid(row=i + 1, column=0, padx=2, pady=3, sticky="nsew")

            row_entries = []
            for j, team in enumerate(self.teams):
                score_entry = tk.Entry(self.game_frame, font=self.base_font, justify="center")
                score_entry.grid(row=i + 1, column=j + 1, padx=2, pady=3, sticky="nsew")
                row_entries.append(score_entry)
            self.score_entries.append(row_entries)

        self.fill_score_entries()

    def fill_score_entries(self):
        for i, team in enumerate(self.teams):
            for j, score in enumerate(self.scores[team]):
                self.score_entries[j][i].delete(0, tk.END)
                self.score_entries[j][i].insert(0, str(score))

    def update_scores(self):
        for i, team in enumerate(self.teams):
            self.totalScore[team] = 0
            for j in range(len(self.games)):
                score = self.score_entries[j][i].get()
                if score:
                    try:
                        if score == "kells" and team == "Coldplay (Mello/Kells)":
                            self.scores[team][j] = 100
                            self.totalScore[team] += 100
                        else:
                            score = int(score)
                            self.scores[team][j] = score
                            self.totalScore[team] += score
                    except ValueError:
                        messagebox.showerror("Input Error", "Please enter valid numeric scores.")
                        return

        self.display_scores()
        self.save_scores()

    def display_scores(self):
        sorted_teams = sorted(self.teams, key=lambda t: self.totalScore[t], reverse=True)
        for index, team in enumerate(sorted_teams):
            self.total_score_labels[f"team_{index}"].config(text=team)
            self.total_score_labels[f"score_{index}"].config(text=str(self.totalScore[team]))

    def save_scores(self):
        with open("scoreboard_data.json", "w") as file:
            json.dump({'scores': self.scores, 'totalScore': self.totalScore}, file)

    def load_scores(self):
        if os.path.exists("scoreboard_data.json"):
            with open("scoreboard_data.json", "r") as file:
                data = json.load(file)
                self.scores = data.get("scores", self.scores)
                self.totalScore = data.get("totalScore", self.totalScore)
        self.teams = sorted(self.teams, key=lambda t: self.totalScore[t], reverse=True)

    def resize_fonts(self, event):
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        new_size = max(7, min(12, int(min(width, height) / 90)))
        self.base_font.configure(size=new_size)
        self.label_font.configure(size=new_size + 1)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScoreboardApp(root)
    root.mainloop()
