
class Tournament:
    def __init__(self, name, location, date, turns, time, description):
        self.name = name
        self.location = location
        self.date = date
        self.turns = turns
        self.list_rounds = []
        self.list_players = []
        #plutot mettre le score d'un joueur dans la classe tournoi pour conserver le score entre chaque tournoi contrairement à la classe player dans lequel elle ne serai pas stocké
        self.time = time
        self.description = description

