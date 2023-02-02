
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
        print(self.list_players)
        self.list_players.sort(key=lambda x: x[0].elo)

    def sort_players_by_score_and_elo(self):
        self.list_players.sort(key=lambda t: (t[1], t[0].elo))

    def sort_player_by_score(self):
        self.list_players.sort(key=lambda x: x[1])

    def update_player_score(self, player, score):
        index = self.get_index(player)
        self.list_players[index][1] += score

    def get_index(self, target):
        for index, x in enumerate(self.list_players):
            if x[0] == target:
                return index
        return -1

    def __str__(self):
        return f"name : {self.name}\n" \
               f"location: {self.location}\n" \
               f"date: {self.date}\n" \
               f"turns : {self.turns}\n" \
               f"time: {self.time}\n" \
               f"description : {self.description}\n"

    def check_if_player_exists(self, player_to_check): #vérifie si le joueur existe déjà dans un tournoi
        if self.list_players is not None:
            for player in self.list_players:
                if player[0] == player_to_check:
                    return True
        return False
