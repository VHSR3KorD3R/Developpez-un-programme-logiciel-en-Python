
class Tournament:
    def __init__(self, name, location, date, turns, time, description):
        self.name = name
        self.location = location
        self.date = date
        self.turns = turns
        self.list_rounds = []
        self.list_players = []
        # plutot mettre le score d'un joueur dans la classe tournoi pour conserver le score entre chaque tournoi contrairement à la classe player dans lequel elle ne serai pas stocké
        self.time = time
        self.description = description

    def sort_players_by_elo(self):
        self.list_players.sort(key=lambda x: x[0].elo)

    def sort_players_by_score_and_elo(self):
        self.list_players.sort(key=lambda t: (t[1], t[0].elo))

    def update_player_score(self, player, score):
        index = self.get_index(player)
        self.list_players[index][1] += score

    def get_index(self, target):
        for index, x in enumerate(self.list_players):
            if x[0] == target:
                return index
        return -1

