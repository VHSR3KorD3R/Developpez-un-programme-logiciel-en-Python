import random
from datetime import date as da

from tinydb import Query

from Controller import db
from Model import Tournament as to, Player as pl, Match as ma, Round as ro
from View.PlayerView import PlayerView
from View.TournamentView import TournamentView


class TournamentManager:
    def __init__(self, view):
        self.tournament = None
        self.view = view
        self.current_turn = 0
        self.static_list_players = self.create_list_players()

    def create_tournament(self, name, location, date, turns, time, description):
        self.tournament = to.Tournament(name, location, date, turns, time, description)
        self.create_list_players()

    def create_list_players(self):
        list_players = []
        for i in range(7):
            player = pl.Player("firstname" + str(i),
                               "last_name" + str(i),
                               "01/01/1970",
                               "F",
                               random.randint(1, 2000))
            list_players.append(player)
        player = pl.Player("x", "last_name1", "01/01/1970", "M", random.randint(1, 2000))
        list_players.append(player)
        return list_players

    def create_first_round(self, name, start_time, nb_players):
        first_round = ro.Round(name, start_time)
        self.tournament.sort_players_by_elo()
        half_nb_players = nb_players // 2
        list_match = []
        for i in range(half_nb_players):
            player1 = self.tournament.list_players[i][0]
            player2 = self.tournament.list_players[half_nb_players + i][0]
            match = ma.Match(player1, player2, 0, 0)
            player1.already_met.append(player2)
            player2.already_met.append(player1)
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
                    self.tournament.list_players[i][0] == self.tournament.list_players[j + 1][0]) and j < \
                        len(self.tournament.list_players) - 2:
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
                           player_info["gender"],
                           player_info["elo"])
        return player

    def find_player(self, list_players):
        player_view = PlayerView()
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
            indice = player_view.get_player_indice()
            player_selected = search_results[indice - 1]
            if self.tournament.check_if_player_exists(player_selected):
                player_view.print_already_exists_player()
            else:
                self.tournament.list_players.append([player_selected, 0])

    def find_player_in_db(self):
        player_view = PlayerView()
        last_name = player_view.search_for_player()
        query = Query()
        list_players_serialized = db.players().search(query.last_name == last_name)
        search_results = []
        for player_serialized in list_players_serialized:
            player = pl.Player.deserialize(player_serialized)
            search_results.append(player)
        if not search_results:
            if player_view.player_not_found() == 'O':
                player_info = player_view.create_player_menu()
                player = self.create_player(player_info)
                db.players().insert(player.serialize())
        else:
            player_view.print_list_players(search_results)
            indice = player_view.get_player_indice()
            player_selected = search_results[indice - 1]
            if self.tournament.check_if_player_exists(player_selected):
                player_view.print_already_exists_player()
            else:
                self.tournament.list_players.append([player_selected, 0])
                db.tournaments().update(self.tournament.serialize(), doc_ids=[self.tournament.id])

    def show_tournament_menu(self, list_players_static, tournament_view):
        choice = tournament_view.print_tournament_menu()
        if choice == 1:
            player_view = PlayerView()
            player_info = player_view.create_player_menu()
            player = self.create_player(player_info)
            self.tournament.list_players.append([player, 0])
            db.players().insert(player)
            list_players_static.append(player)
            return self.show_tournament_menu(list_players_static, tournament_view)
        elif choice == 2:
            self.find_player_in_db()
            return self.show_tournament_menu(list_players_static, tournament_view)
        elif choice == 3:
            if self.tournament.list_players is not None:
                self.tournament.sort_player_by_name()
                tournament_view.print_ranking(self.tournament.list_players)
            else:
                print("pas de joueurs encore inscrit")
            return self.show_tournament_menu(list_players_static, tournament_view)
        elif choice == 4:
            nb_rounds = self.tournament.turns
            if self.tournament.current_turn < nb_rounds:
                if self.tournament.current_turn == 0:
                    today = da.today()
                    date = today.strftime("%d/%m/%Y")
                    nb_players = len(self.tournament.list_players)
                    self.create_first_round("round 1", date, nb_players)
                else:
                    today = da.today()
                    date = today.strftime("%d/%m/%Y")
                    self.create_rounds("round " + str(self.tournament.current_turn + 1), date)

            tournament_view.print_list_match(self.tournament.list_rounds[self.tournament.current_turn].list_match)
            return self.show_tournament_menu(list_players_static, tournament_view)
        elif choice == 5:
            if self.tournament.list_rounds or self.tournament.current_turn == self.tournament.turns:
                for match in self.tournament.list_rounds[self.tournament.current_turn].list_match:
                    player1_fullname = match.player1.last_name + " " + match.player1.first_name
                    player2_fullname = match.player2.last_name + " " + match.player2.first_name
                    choice = tournament_view.print_round_editor(player1_fullname, player2_fullname)
                    if choice == 1:
                        match.player1_score = 1
                        match.player2_score = 0
                        for player in self.tournament.list_players:
                            if player[0] == match.player1:
                                player[1] += 1
                                break

                    elif choice == 2:
                        match.player1_score = 0
                        match.player2_score = 1
                        for player in self.tournament.list_players:
                            if player[0] == match.player1:
                                player[1] += 1
                                break

                    elif choice == 3:
                        match.player1_score = 0.5
                        match.player2_score = 0.5
                        for player in self.tournament.list_players:
                            if player[0] == match.player1:
                                player[1] += 0.5
                            elif player[1] == match.player2:
                                player[1] += 0.5
                self.tournament.current_turn += 1
                if self.tournament.current_turn == self.tournament.turns:
                    self.tournament.is_ongoing = False
                db.tournaments().update(self.tournament.serialize(), doc_ids=[self.tournament.id])
            return self.show_tournament_menu(list_players_static, tournament_view)

        elif choice == 6:
            self.tournament.sort_player_by_score()
            tournament_view.print_ranking(self.tournament.list_players)
            return self.show_tournament_menu(list_players_static, tournament_view)

        elif choice == 0:
            db.tournaments().update(self.tournament.serialize(), doc_ids=[self.tournament.id])
            return 0

    def run(self):
        list_players_static = self.create_list_players()
        # for player in list_players_static:
        #     print(player.last_name)
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
                # for player in list_players_static:
                #     self.tournament.list_players.append([player, 0])
                tournament_id = db.tournaments().insert(self.tournament.serialize())
                self.tournament.id = tournament_id
                self.show_tournament_menu(list_players_static, tournament_view)
            elif choice == 2:
                tournament_view = TournamentView()
                query = Query()
                tournament_list = db.tournaments().search(query.is_ongoing == True)
                tournament_view.print_ongoing_tournament(tournament_list)
                indice = tournament_view.get_tournament_indice()
                tournament_selected = tournament_list[indice - 1]
                self.tournament = to.Tournament.deserialize(tournament_selected)
                print(self.tournament)
                self.show_tournament_menu(list_players_static, tournament_view)
            elif choice == 3:
                player_view = PlayerView()
                player_info = player_view.create_player_menu()
                player = self.create_player(player_info)
                db.players().insert(player.serialize())
                list_players_static.append(player)

            elif choice == 4:
                players = db.players().all()
                if players is not None:
                    player_view = PlayerView()
                    player_view.print_list_player(players)
                else:
                    print("pas de joueurs crée")

            elif choice == 5:
                tournaments = db.tournaments().all()
                if tournaments is not None:
                    tournament_view = TournamentView()
                    tournament_view.print_tournament_list(tournaments)
                else:
                    print("pas de tournois crée")
