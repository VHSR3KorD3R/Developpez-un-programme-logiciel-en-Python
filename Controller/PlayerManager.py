from Model import Player as pl
#enlever les managers qui ne rajoutent pas grand chose on peut directement faire ça dans le main soit dans le tournoi manager

class PlayerManager:
    def __init__(self, list_players: list):
        self.list_players = list_players

    def create_player(self, first_name, last_name, birthdate, elo):
        player = pl.Player(first_name, last_name, birthdate, elo)
        self.list_players.append(player)

    def get_all_players(self):
        return self.list_players

    def sort_players_by_elo(self):
        self.list_players.sort(key=self.get_elo)

    def sort_players_by_score(self):
        self.list_players.sort(key=lambda t: (t.elo, t.score))

    def get_elo(self, player: pl.Player):
        return player.elo

    def get_score(self, player: pl.Player):
        return player.score
