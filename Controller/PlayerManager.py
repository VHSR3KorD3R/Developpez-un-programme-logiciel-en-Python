from Model import Player as pl


class PlayerManager:
    def __init__(self, player, list_players: list):
        self.player = player
        self.list_players = list_players

    def create_player(self, first_name, last_name, birthdate, elo):
        self.player = pl.Player(first_name, last_name, birthdate, elo, 0)
        self.list_players.append(self.player)

    def get_all_players(self):
        return self.list_players

