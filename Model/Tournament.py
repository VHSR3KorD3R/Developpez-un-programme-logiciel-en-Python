from Model import Round as ro, Player as pl

from Controller import db


class Tournament:
    def __init__(self,
                 name,
                 location,
                 date,
                 turns,
                 time,
                 description,
                 id=None,
                 is_ongoing=True,
                 current_turn=0):
        self.name = name
        self.location = location
        self.date = date
        self.turns = turns
        self.list_rounds = []
        self.list_players = []
        # plutot mettre le score d'un joueur dans la classe tournoi pour conserver le score entre chaque tournoi
        # contrairement à la classe player dans lequel elle ne serai pas stocké
        self.time = time
        self.description = description
        self.id = id
        self.is_ongoing = is_ongoing
        self.current_turn = current_turn

    def serialize(self):
        serialized_list_rounds = []
        if self.list_rounds is not None:
            for round in self.list_rounds:
                serialized_list_rounds.append(round.serialize())

        id_list_players = []
        if self.list_players is not None:
            for player in self.list_players:
                player_id = player[0].id
                tmp: dict = {
                    "player_id": player_id,
                    "player_score": player[1]
                }
                id_list_players.append(tmp)

        tournament: dict = {
            "name": self.name,
            "location": self.location,
            "date": self.date,
            "turns": self.turns,
            "list_rounds": serialized_list_rounds,
            "list_players": id_list_players,
            "time": self.time,
            "description": self.description,
            "is_ongoing": self.is_ongoing,
            "current_turn": self.current_turn
        }
        return tournament

    @staticmethod
    def deserialize(tournament_serialized):
        deserialized_list_players = []

        for player_id in tournament_serialized["list_players"]:
            serialized_player = db.players().get(doc_id=player_id["player_id"])
            deserialized_list_players.append([pl.Player.deserialize(serialized_player), player_id["player_score"]])

        deserialized_list_rounds = []

        for serialized_round in tournament_serialized["list_rounds"]:
            deserialized_list_rounds.append(ro.Round.deserialize(serialized_round))

        deserialized_tournament = Tournament(
            name=tournament_serialized["name"],
            location=tournament_serialized["location"],
            date=tournament_serialized["date"],
            turns=tournament_serialized["turns"],
            time=tournament_serialized["time"],
            id=tournament_serialized.doc_id,
            description=tournament_serialized["description"],
            is_ongoing=tournament_serialized["is_ongoing"],
            current_turn=tournament_serialized["current_turn"]

        )
        deserialized_tournament.list_players = deserialized_list_players
        deserialized_tournament.list_rounds = deserialized_list_rounds
        return deserialized_tournament

    def sort_players_by_elo(self):
        self.list_players.sort(key=lambda x: x[0].elo)

    def sort_players_by_score_and_elo(self):
        self.list_players.sort(key=lambda t: (t[1], t[0].elo))

    def sort_player_by_score(self):
        self.list_players.sort(key=lambda x: x[1], reverse=True)

    def sort_player_by_name(self):
        if self.list_players is not None:
            self.list_players.sort(key=lambda x: x[0].last_name)

    def update_player_score(self, player, score):
        index = self.get_index(player)
        self.list_players[index][1] += score

    def get_index(self, target):
        for index, x in enumerate(self.list_players):
            if x[0] == target:
                return index
        return None

    def __str__(self):
        return f"name : {self.name}\n" \
               f"location: {self.location}\n" \
               f"date: {self.date}\n" \
               f"turns : {self.turns}\n" \
               f"time: {self.time}\n" \
               f"description : {self.description}\n"

    # vérifie si le joueur existe déjà dans un tournoi
    def check_if_player_exists(self, player_to_check):
        if self.list_players is not None:
            for player in self.list_players:
                if player[0] == player_to_check:
                    return True
        return False
