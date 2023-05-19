import random
from datetime import date as da

from tinydb import Query
import pandas as pd

from Controller import db
from Model import Tournament as to, Player as pl, Match as ma, Round as ro
from View.PlayerView import PlayerView
from View.TournamentView import TournamentView

NO_PLAYER_ERROR = 0
NOT_ENOUGH_PLAYERS = 1
MAX_PLAYERS_ERROR = 3
NO_TOURNAMENT_CREATED = 4
MAX_ROUND_ERROR = 5


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
                if self.tournament.list_players[i][0].id in list_players_matched and i < len(
                        self.tournament.list_players) - 2:
                    i += 1
                if (self.tournament.list_players[j + 1][0].id in list_players_matched or
                    self.tournament.list_players[i][0] == self.tournament.list_players[j + 1][0]) and j < \
                        len(self.tournament.list_players) - 2:
                    j += 1
                if self.tournament.list_players[i][0] not in self.tournament.list_players[j + 1][0].already_met and \
                        len(list_match) <= 3:
                    match = ma.Match(self.tournament.list_players[i][0], self.tournament.list_players[j + 1][0], 0, 0)
                    self.tournament.list_players[i][0].already_met.append(self.tournament.list_players[j + 1][0])
                    self.tournament.list_players[j + 1][0].already_met.append(self.tournament.list_players[i][0])
                    list_match.append(match)
                    list_players_matched.append(self.tournament.list_players[i][0].id)
                    list_players_matched.append(self.tournament.list_players[j + 1][0].id)
                    break
                else:
                    j += 1
            i += 1
        if self.tournament.list_players[6][0] in self.tournament.list_players[7][0].already_met and\
                len(self.tournament.list_rounds) == 3 and len(list_match) == 3:
            if list_match[2].player1 not in self.tournament.list_players[6][0].already_met \
                    and list_match[2].player2 not in self.tournament.list_players[7][0].already_met:
                list_match.pop(2)
                if list_match[2].player1 != self.tournament.list_players[6][0] and\
                        list_match[2].player1 not in self.tournament.list_players[6][0] and\
                        list_match[2].player2 != self.tournament.list_players[7][0] and\
                        list_match[2].player2 not in self.tournament.list_players[7][0].already_met:
                    match1 = ma.Match(list_match[2].player1, self.tournament.list_players[6][0], 0,
                                      0)
                    match2 = ma.Match(list_match[2].player2, self.tournament.list_players[7][0], 0,
                                      0)
                    list_match.append(match1)
                    list_match.append(match2)
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
                player_view.print_player_created()
        else:
            player_view.print_list_players(search_results)
            indice = player_view.get_player_indice()
            player_selected = search_results[indice - 1]
            if self.tournament.check_if_player_exists(player_selected):
                player_view.print_already_exists_player()
            else:
                self.tournament.list_players.append([player_selected, 0])
                db.tournaments().update(self.tournament.serialize(), doc_ids=[self.tournament.id])
                player_view.print_player_added()

    def create_player_menu(self, tournament_view):
        if len(self.tournament.list_players) >= 8:
            tournament_view.tournament_error(MAX_PLAYERS_ERROR)
        else:
            player_view = PlayerView()
            player_info = player_view.create_player_menu()
            player = self.create_player(player_info)
            self.tournament.list_players.append([player, 0])
            query = Query()
            player_serialized = player.serialize()
            db.players().insert(player_serialized)
            player_serialized = db.players().get((query.last_name == player.last_name) &
                                                 (query.first_name == player.first_name) &
                                                 (query.birthdate == player.birthdate))
            player.id = player_serialized.doc_id
            db.players().update(player.serialize(), doc_ids=[player.id])
            db.tournaments().update(self.tournament.serialize(), doc_ids=[self.tournament.id])
            player_view.print_player_created()

    def add_player_to_tournament(self, tournament_view):
        if len(self.tournament.list_players) >= 8:
            tournament_view.tournament_error(MAX_PLAYERS_ERROR)
        else:
            self.find_player_in_db()

    def print_list_player(self, tournament_view):
        if self.tournament.list_players is None or len(self.tournament.list_players) == 0:
            tournament_view.tournament_error(NO_PLAYER_ERROR)
        else:
            self.tournament.sort_player_by_name()
            tournament_view.print_ranking(self.tournament.list_players)

    def print_round(self, tournament_view):
        nb_rounds = self.tournament.turns
        if self.tournament.current_turn >= nb_rounds:
            tournament_view.tournament_error(MAX_ROUND_ERROR)
        elif len(self.tournament.list_players) < 8:
            tournament_view.tournament_error(NOT_ENOUGH_PLAYERS)
        else:
            if self.tournament.current_turn == 0:
                today = da.today()
                date = today.strftime("%d/%m/%Y")
                nb_players = len(self.tournament.list_players)
                self.create_first_round("round 1", date, nb_players)
            else:
                today = da.today()
                date = today.strftime("%d/%m/%Y")
                self.create_rounds("round " + str(self.tournament.current_turn + 1), date)
            tournament_view.print_list_match2(self.tournament.list_rounds[self.tournament.current_turn].list_match)
        self.view.print_round_created()

    def enter_round_results(self, tournament_view):
        if self.tournament.current_turn >= 4:
            tournament_view.tournament_error(MAX_ROUND_ERROR)
        elif len(self.tournament.list_rounds) != 0 or self.tournament.current_turn == self.tournament.turns:
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
                        if player[0] == match.player2:
                            player[1] += 1
                            break
                elif choice == 3:
                    match.player1_score = 0.5
                    match.player2_score = 0.5
                    for player in self.tournament.list_players:
                        if player[0] == match.player1:
                            player[1] += 0.5
                        elif player[0] == match.player2:
                            player[1] += 0.5
            self.tournament.current_turn += 1
            if self.tournament.current_turn == self.tournament.turns:
                self.tournament.is_ongoing = False
            today = da.today()
            date = today.strftime("%d/%m/%Y")
            current_round = self.tournament.list_rounds[self.tournament.current_turn - 1]
            current_round.end_time = date
            db.tournaments().update(self.tournament.serialize(), doc_ids=[self.tournament.id])

    def print_players_rank(self, tournament_view):
        self.tournament.sort_players_by_score_and_elo()
        tournament_view.print_ranking(self.tournament.list_players)

    def show_tournament_menu(self, tournament_view):
        choice = tournament_view.print_tournament_menu()
        if choice == 1:  # Création d'un joueur
            self.create_player_menu(tournament_view)
            return self.show_tournament_menu(tournament_view)
        elif choice == 2:  # Ajouter un joueur
            self.add_player_to_tournament(tournament_view)
            return self.show_tournament_menu(tournament_view)
        elif choice == 3:
            self.print_list_player(tournament_view)
            return self.show_tournament_menu(tournament_view)
        elif choice == 4:
            self.print_round(tournament_view)
            return self.show_tournament_menu(tournament_view)
        elif choice == 5:
            self.enter_round_results(tournament_view)
            return self.show_tournament_menu(tournament_view)
        elif choice == 6:
            self.print_players_rank(tournament_view)
            return self.show_tournament_menu(tournament_view)
        elif choice == 0:
            db.tournaments().update(self.tournament.serialize(), doc_ids=[self.tournament.id])
            return 0

    def create_tournament(self):
        tournament_view = TournamentView()
        tournament_info = tournament_view.create_tournament_menu()
        self.tournament = to.Tournament(tournament_info["name"],
                                        tournament_info["location"],
                                        tournament_info["date"],
                                        tournament_info["turns"],
                                        tournament_info["time"],
                                        tournament_info["description"])
        tournament_id = db.tournaments().insert(self.tournament.serialize())
        self.tournament.id = tournament_id
        tournament_view.print_tournament_created()
        self.show_tournament_menu(tournament_view)

    def resume_tournament(self):
        tournament_view = TournamentView()
        query = Query()
        tournament_list = db.tournaments().search(query.is_ongoing == 1)
        if len(tournament_list) > 0:
            tournament_view.print_ongoing_tournament(tournament_list)
            indice = tournament_view.get_tournament_indice(len(tournament_list))
            tournament_selected = tournament_list[indice - 1]
            self.tournament = to.Tournament.deserialize(tournament_selected)
            self.show_tournament_menu(tournament_view)

    def create_player_outside_tournament(self):
        query = Query()
        player_view = PlayerView()
        player_info = player_view.create_player_menu()
        player = self.create_player(player_info)
        player_serialized = player.serialize()
        db.players().insert(player_serialized)
        db.players().update({'id': player_serialized.doc_id}, query.doc_id == player_serialized.doc_id)
        tournament_view = TournamentView()
        player_view.print_player_created()
        self.show_tournament_menu(tournament_view)

    def print_reports(self):
        report_choice = self.view.print_reports()
        if report_choice == 1:
            players = db.players().all()
            self.view.print_list_players(players)
        elif report_choice == 2:
            tournaments = db.tournaments().all()
            self.view.print_list_tournament(tournaments)
            pd.DataFrame(tournaments)
        elif report_choice == 3:
            name = self.view.search_tournament()
            query = Query()
            list_tournament = db.tournaments().search(query.name.search(name))
            self.view.print_list_tournament(list_tournament)
            choice_tournament = self.view.chose_tournament()
            # tournament = to.Tournament.deserialize(list_tournament[choice])
            choice_report = self.view.print_choice_reports()
            if choice_report == 1:
                list_players = list_tournament[choice_tournament]["list_players"]
                players = []
                for player_serialized in list_players:
                    player = db.players().get(doc_id=player_serialized["player_id"])
                    player["score"] = player_serialized["player_score"]
                    players.append(player)
                self.view.print_list_players(players)
            elif choice_report == 2:
                self.view.print_tournament(list_tournament[choice_tournament])
            elif choice_report == 3:
                self.view.print_tournament_info(list_tournament[choice_tournament])

    def run(self):
        while True:
            choice = self.view.print_menu()
            if choice == 1:
                self.create_tournament()
            elif choice == 2:
                self.resume_tournament()
            elif choice == 3:
                self.create_player_outside_tournament()
            elif choice == 4:
                players = db.players().all()
                player_view = PlayerView()
                if len(players) > 0:
                    player_view.print_list_player(players)
                else:
                    player_view.print_error()

            elif choice == 5:
                tournaments = db.tournaments().all()
                tournament_view = TournamentView()
                if len(tournaments) > 0:
                    tournament_view.print_tournament_list(tournaments)
                else:
                    tournament_view.tournament_error(NO_TOURNAMENT_CREATED)

            elif choice == 6:
                self.print_reports()
