class Match:
    def __init__(self, player1, player2, player1_score, player2_score):
        self.player1 = player1
        self.player2 = player2
        self.player1_score = player1_score
        self.player2_score = player2_score

    def __str__(self):
        return f"player1 : {self.player1.first_name}\n" \
               f"player2: {self.player2.first_name}\n" \
               f"player1_score: {self.player1_score}\n" \
               f"player2_score : {self.player2_score}\n"
