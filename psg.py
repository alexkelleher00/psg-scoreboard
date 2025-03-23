import tkinter as tk
from tkinter import messagebox
import json
import os

class ScoreboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PSG ScoreBoard")

        # Fixed list of teams and games
        self.teams = ["Team A", "Team B", "Team C", "Team D", "Team E", "Team F", "Team G", "Team H"]
        self.games = ["Volleyball", "Treasure Hunt", 
                      "Pickleball", "3 Point Contest", 
                      "Bumper Ball", "Waiter Games",
                      "Water Game", "Marbles",
                       "Sling Shot", "Obstacle Course"]
        
        self.score_entries = []
        # Initialize a dictionary to hold the scores for each team and game (10 games)
        self.scores = {team: [0] * 10 for team in self.teams}
        self.totalScore = {team: 0 for team in self.teams}

        self.load_scores()

        # Create the layout for teams, games, and total scores
        self.create_ui()

    def create_ui(self):
        # Main frame for the game scores
        self.game_frame = tk.Frame(self.root)
        self.game_frame.grid(row=0, column=0, padx=10, pady=10)

        # Create labels for team names (displayed at the top)
        for col, team in enumerate(self.teams):
            team_label = tk.Label(self.game_frame, text=team, width=10, relief="solid")
            team_label.grid(row=0, column=col + 1, padx=5, pady=5)

        self.create_game_slots()

        # Button to update and display scores
        update_button = tk.Button(self.root, text="Update Scores", command=self.update_scores)
        update_button.grid(row=2, column=0, columnspan=len(self.teams), pady=10)

        # Frame for displaying total scores and ranking
        self.total_score_frame = tk.Frame(self.root)
        self.total_score_frame.grid(row=0, column=1, padx=10, pady=10)

        for i, team in enumerate(self.teams):
            self.place_labels = tk.Label(self.total_score_frame, text=f"{i+1}: ", font=("Arial", 14))
            self.place_labels.grid(row=i+1, column=0, padx=5, pady=5)
    
        # Display total score for each team
        self.total_score_labels = {}
        for i, team in enumerate(self.teams):
            team_label = tk.Label(self.total_score_frame, text=f"{team}: {self.totalScore[team]}", width=20, relief="solid")
            team_label.grid(row=i + 1, column=1, padx=10, pady=5)
            self.total_score_labels[team] = team_label

    def create_game_slots(self):
        # Create rows for games
        for i, game in enumerate(self.games):
            game_label = tk.Label(self.game_frame, text=game, width=20, relief="solid")
            game_label.grid(row=i + 1, column=0, padx=5, pady=5)

            # Create entry fields for each game and team to input scores
            row_entries = []
            for j, team in enumerate(self.teams):
                score_entry = tk.Entry(self.game_frame, width=5)
                score_entry.grid(row=i + 1, column=j + 1, padx=5, pady=5)
                row_entries.append(score_entry)
            self.score_entries.append(row_entries)

            # Fill in the entry boxes with the saved scores
        self.fill_score_entries()

    def fill_score_entries(self):
        # Refill the score entries with the saved score data
        for i, team in enumerate(self.teams):
            for j, score in enumerate(self.scores[team]):
                self.score_entries[j][i].delete(0, tk.END)  # Clear any existing text
                self.score_entries[j][i].insert(0, str(score))  # Insert the saved score

    def update_scores(self):
        # Loop over the score entries and store values in the dictionary
        
        for i, team in enumerate(self.teams):
            self.totalScore[team] = 0
            for j, game in enumerate(self.scores[team]):
                score = self.score_entries[j][i].get()
                if score:
                    try:
                        score = int(score)
                        self.scores[team][j] = score
                        self.totalScore[team] += score
                    except ValueError:
                        messagebox.showerror("Input Error", "Please enter valid numeric scores.")
                        return

        self.display_scores()
        self.save_scores()

    def display_scores(self):
       # Sort the teams based on their total score in descending order
        sorted_teams = sorted(self.teams, key=lambda team: self.totalScore[team], reverse=True)

        # Update the total score labels dynamically based on sorted teams
        for index, team in enumerate(sorted_teams):
            self.total_score_labels[team].config(text=f"{team}: {self.totalScore[team]}")
            self.total_score_labels[team].grid(row=index + 1, column=1, padx=10, pady=5)
    

    def save_scores(self):
        # Save the scores and total scores to a file
        data = {
            'scores': self.scores,
            'totalScore': self.totalScore
        }

        with open("scoreboard_data.json", "w") as file:
            json.dump(data, file)
            print("Scores saved to file.")

    def load_scores(self):
        # Load the scores and total scores from the file if it exists
        if os.path.exists("scoreboard_data.json"):
            with open("scoreboard_data.json", "r") as file:
                data = json.load(file)
                self.scores = data.get("scores", self.scores)
                self.totalScore = data.get("totalScore", self.totalScore)
                print("Scores loaded from file.")
        else:
            print("No previous scores found, starting with default values.")
        
        self.teams = sorted(self.teams, key=lambda team: self.totalScore[team], reverse=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScoreboardApp(root)
    root.mainloop()