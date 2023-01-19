import random
from Model import Tournament as to, Player as pl, Match as ma, Round as ro
from View.PlayerView import PlayerView
from View.TournamentView import TournamentView


class TournamentManager:
    def __init__(self, view):
        self.tournament = None
        self.view = view

    def create_tournament(self, name, location, date, turns, time, description):
        self.tournament = to.Tournament(name, location, date, turns, time, description)
        self.create_list_players()

    def create_list_players(self):
        list_players = []
        for i in range(8):
            tmp_list = []
            player = pl.Player("firstname " + str(i),
                               "last_name" + str(i),
                               "01/01/1970",
                               random.randint(1, 2000))
            tmp_list.append(player)
            tmp_list.append(0)
            list_players.append(tmp_list)
        return list_players

    def create_first_round(self, name, start_time, nb_players):
        first_round = ro.Round(name, start_time)
        self.tournament.sort_players_by_elo()
        half_nb_players = len(nb_players) // 2
        list_match = []
        for i in range(half_nb_players):
            player1 = self.tournament.list_players[i][0]
            player2 = self.tournament.list_players[half_nb_players + i][0]
            match = ma.Match(player1, player2, 0, 0)
            player1.add_already_met_list(player2)
            player2.add_already_met_list(player1)
            list_match.append(match)
        first_round.list_match = list_match
        self.tournament.list_rounds.append(first_round)

    def create_rounds(self, name, start_time):
        self.tournament.sort_players_by_score_and_elo()
        n_round = ro.Round(name, start_time)
        i = 0
        list_players_matched = []
        list_match = []
        while i < len(self.tournament.list_players) - 1:
            j = i
            while j < len(self.tournament.list_players) - 1:
                if self.tournament.list_players[i][0] in list_players_matched and i < len(
                        self.tournament.list_players) - 2:
                    i += 1
                if (self.tournament.list_players[j + 1][0] in list_players_matched or
                    self.tournament.list_players[i][0] == self.tournament.list_players[j + 1][0]) and j < len(
                    self.tournament.list_players) - 2:
                    j += 1
                if self.tournament.list_players[i][0] not in self.tournament.list_players[j + 1][0].already_met:
                    match = ma.Match(self.tournament.list_players[i][0], self.tournament.list_players[j + 1][0], 0, 0)
                    self.tournament.list_players[i][0].already_met.append(self.tournament.list_players[j + 1][0])
                    self.tournament.list_players[j + 1][0].already_met.append(self.tournament.list_players[i][0])
                    list_match.append(match)
                    list_players_matched.append(self.tournament.list_players[i][0])
                    list_players_matched.append(self.tournament.list_players[j + 1][0])
                    break
                else:
                    j += 1
            i += 1
        n_round.list_match = list_match
        self.tournament.list_rounds.append(n_round)

    def create_player(self, player_info):
        tmp_list = []
        player = pl.Player(player_info["first_name"],
                           player_info["last_name"],
                           player_info["birthdate"],
                           player_info["elo"])
        tmp_list.append(player)
        tmp_list.append(0)
        return tmp_list

    def find_player(self, list_players, player_view):
        last_name = player_view.search_for_player()
        search_results = []
        for player in list_players:
            if player[0].last_name == last_name:
                search_results.append(player)
                print(search_results)
        if not search_results:
            if player_view.player_not_found() == 'O':
                player_info = player_view.create_player_menu()
                self.create_player(player_info)
            else:
                return 0

    def run(self):
        list_players_static = self.create_list_players()
        for player in list_players_static:
            print(player[0].last_name)
        while True:
            choice = self.view.print_menu()
            if choice == "1":
                tournament_view = TournamentView()
                tournament_info = tournament_view.create_tournament_menu()
                self.tournament = to.Tournament(tournament_info["name"],
                                                tournament_info["location"],
                                                tournament_info["date"],
                                                tournament_info["turns"],
                                                tournament_info["time"],
                                                tournament_info["description"])
                player_view = PlayerView()
                self.find_player(list_players_static, player_view)

            elif choice == "2":
                player_view = PlayerView()
                player_info = player_view.create_player_menu()
                self.create_player(player_info)
