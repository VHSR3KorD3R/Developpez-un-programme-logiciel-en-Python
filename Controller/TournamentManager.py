import random
from datetime import date as da

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
            player = pl.Player("firstname" + str(i),
                               "last_name" + str(i),
                               "01/01/1970",
                               random.randint(1, 2000))
            list_players.append(player)
        player = pl.Player("x", "last_name1", "01/01/1970", random.randint(1,2000))
        list_players.append(player)
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
        player = pl.Player(player_info["first_name"],
                           player_info["last_name"],
                           player_info["birthdate"],
                           player_info["elo"])
        return player

    def find_player(self, list_players, player_view):
        last_name = player_view.search_for_player()
        search_results = []
        for player in list_players:
            if player.last_name == last_name:
                search_results.append(player)
        if not search_results:
            if player_view.player_not_found() == 'O':
                player_info = player_view.create_player_menu()
                self.create_player(player_info)
        else:
            player_view.print_list_players(search_results)
            indice = player_view.get_player_indice(search_results)
            return search_results[indice - 1]

    def show_tournament_menu(self, list_players_static, tournament_view):
        choice = tournament_view.print_tournament_menu()
        if choice == 1:
            player_view = PlayerView()
            player_info = player_view.create_player_menu()
            player = self.create_player(player_info)
            self.tournament.list_players.append([player, 0])
            list_players_static.append(player)
            return self.show_tournament_menu(list_players_static, tournament_view)
        elif choice == 2:
            player_view = PlayerView()
            player = self.find_player(list_players_static, player_view)
            self.tournament.list_players.append([player, 0])
            return self.show_tournament_menu(list_players_static, tournament_view)
        elif choice == 3:
            print(self.tournament.list_players)
            for player, score in self.tournament.list_players:
                print(player)
            return self.show_tournament_menu(list_players_static, tournament_view)
        elif choice == 4:
            nb_rounds = self.tournament.turns
            for i in nb_rounds:
                if i == 0:
                    today = da.today()
                    date = today.strftime("%d/%m/%Y")
                    self.create_first_round("premier round", date, 8)
                else:
                    self.create_rounds()
        elif choice == 5:
            return 0

    def run(self):
        list_players_static = self.create_list_players()
        for player in list_players_static:
            print(player.last_name)
        while True:
            choice = self.view.print_menu()
            if choice == 1:
                tournament_view = TournamentView()
                tournament_info = tournament_view.create_tournament_menu()
                self.tournament = to.Tournament(tournament_info["name"],
                                                tournament_info["location"],
                                                tournament_info["date"],
                                                tournament_info["turns"],
                                                tournament_info["time"],
                                                tournament_info["description"])
                self.show_tournament_menu(list_players_static, tournament_view)

            elif choice == 2:
                player_view = PlayerView()
                player_info = player_view.create_player_menu()
                player = self.create_player(player_info)
                list_players_static.append(player)

            elif choice == 3:
                for player in list_players_static:
                    print(player)

            elif choice == 4:
                if self.tournament is not None:
                    print(self.tournament)
                else:
                    print("pas de tournois crée")
