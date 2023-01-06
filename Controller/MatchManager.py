from Model import Match as ma


class MatchManager:
    def __init__(self):
        self.match = None

    def create_match(self, player1, player2, player1_score, player2_score):
        self.match = ma.Match(player1, player2, player1_score, player2_score)

    def update_match(self, player1_score, player2_score):
        self.match.player1_score = player1_score
        self.match.player2_score = player2_score
