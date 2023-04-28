from Controller import db
from Model import Player as pl


class Match:
    def __init__(self, player1=None, player2=None, player1_score=None, player2_score=None):
        self.player1 = player1
        self.player2 = player2
        self.player1_score = player1_score
        self.player2_score = player2_score

    def __str__(self):
        return f"player1: {self.player1.first_name} {self.player1.last_name}\n" \
               f"player2: {self.player2.first_name} {self.player2.last_name}\n" \
               f"player1_score: {self.player1_score}\n" \
               f"player2_score: {self.player2_score}"

    def serialize(self):
        match: dict = {
            "player1": self.player1.id,
            "player2": self.player2.id,
            "player1_score": self.player1_score,
            "player2_score": self.player2_score
        }
        return match

    @staticmethod
    def deserialize(serialized_match):
        player1_serialized = db.players().get(doc_id=serialized_match["player1"])
        player1 = pl.Player.deserialize(player1_serialized)
        player2_serialized = db.players().get(doc_id=serialized_match["player2"])
        player2 = pl.Player.deserialize(player2_serialized)

        deserialized_match = Match(
            player1=player1,
            player2=player2,
            player1_score=serialized_match["player1_score"],
            player2_score=serialized_match["player2_score"]
        )
        return deserialized_match
