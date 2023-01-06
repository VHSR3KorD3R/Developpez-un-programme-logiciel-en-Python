import random
from Model import Tournament as to, Player as pl, Match as ma, Round as ro
from Controller import PlayerManager as pm
from View import PlayerView as plv

class TournamentManager:
    def __init__(self):
        self.list_players = []
        self.list_match = []
        self.list_rounds = []
        self.tournament = None

    def create_tournament(self, name, location, date, turns, time, description):
        self.tournament = to.Tournament(name, location, date, turns, time, description)
        self.create_list_players()
        self.create_first_round("first round", "01/01/1970", self.list_players)

    def create_list_players(self):
        for i in range(8):
            tmp_list = []
            player = pl.Player("firstname " + str(i),
                               "last_name" + str(i),
                               "01/01/1970",
                               random.randint(1, 2000))
            tmp_list.append(player)
            tmp_list.append(0)
            self.list_players.append(tmp_list)

    def create_first_round(self, name, start_time, list_players):
        first_round = ro.Round(name, start_time)
        self.sort_players_by_elo()
        half_nb_players = len(list_players) // 2
        list_match = []
        for i in range(half_nb_players):
            player1 = self.list_players[i][0]
            player2 = self.list_players[half_nb_players + i][0]
            match = ma.Match(player1, player2, 0, 0)
            player1.add_already_met_list(player2)
            player2.add_already_met_list(player1)
            list_match.append(match)
        first_round.list_match = list_match
        self.list_rounds.append(first_round)

    def create_rounds(self, name, start_time):
        self.sort_players_by_score_and_elo()
        n_round = ro.Round(name, start_time)
        i = 0
        list_players_matched = []
        list_match = []
        while i < len(self.list_players) - 1:
            j = i
            while j < len(self.list_players) - 1:
                if self.list_players[i][0] in list_players_matched and i < len(self.list_players) - 2:
                    i += 1
                if (self.list_players[j + 1][0] in list_players_matched or
                    self.list_players[i][0] == self.list_players[j + 1][0]) and j < len(self.list_players) - 2:
                    j += 1
                if self.list_players[i][0] not in self.list_players[j + 1][0].already_met:
                    match = ma.Match(self.list_players[i][0], self.list_players[j + 1][0], 0, 0)
                    self.list_players[i][0].already_met.append(self.list_players[j + 1][0])
                    self.list_players[j + 1][0].already_met.append(self.list_players[i][0])
                    list_match.append(match)
                    list_players_matched.append(self.list_players[i][0])
                    list_players_matched.append(self.list_players[j + 1][0])
                    break
                else:
                    j += 1
            i += 1
        n_round.list_match = list_match
        self.list_rounds.append(n_round)

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
