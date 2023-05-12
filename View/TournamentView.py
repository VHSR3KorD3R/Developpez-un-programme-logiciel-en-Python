from Controller import InputChecker as ic
from datetime import date as da
from Controller import TournamentManager
from Controller import db

import pandas as pd
from tinydb import Query



class TournamentView:
    def create_tournament_menu(self):
        name = ic.check_user_input("Nom du tournoi: ")
        location = ic.check_user_input("Lieu du tournoi: ")
        today = da.today()
        date = today.strftime("%d/%m/%Y")
        turns = ic.check_number_input("nombre de rounds: ")
        time = ic.check_time_control("Controle du temps: ")
        description = ic.check_user_input("Description: ")
        return {"name": name,
                "location": location,
                "date": date,
                "turns": turns,
                "time": time,
                "description": description
                }

    def print_tournament_menu(self):
        print("Menu tournoi")
        print("[1] Créer un nouveau joueur à inscrire")
        print("[2] Inscrire un joueur")
        print("[3] Afficher la liste des inscris au tournoi")
        print("[4] Créer un tour")
        print("[5] Saisir les résultats du tour en cours")
        print("[6] Voir le classment")
        print("[0] Sortir")

        return ic.check_number_input("choix: ")

    def print_round_editor(self, player1_name, player2_name):
        print("sélectionnez le vainqueur du match:")
        print("[1] " + player1_name)
        print("[2] " + player2_name)
        print("ou alors [3] pour match nul")

        choice = ic.check_number_input("choix: ")
        if choice < 4:
            return choice
        else:
            self.print_round_editor(player1_name, player1_name)

    def print_list_match(self, list_match):
        players1 = ""
        players2 = ""
        players1_scores = ""
        players2_scores = ""
        for match in list_match:
            player1, player2, player1_score, player2_score = match.__str__().split("\n")
            players1 += player1 + "."
            players2 += player2 + "."

        max_player1_length = max(map(len, players1.strip().split(".")))
        max_player2_length = max(map(len, players2.strip().split(".")))

        max_length = max(max_player1_length, max_player2_length)
        players1 = ""
        players2 = ""

        for match in list_match:
            player1, player2, player1_score, player2_score = match.__str__().split("\n")
            players1 += player1 + "\t\t" + (" " * (max_length - len(player1)))
            players2 += player2 + "\t\t" + (" " * (max_length - len(player2)))
            players1_scores += player1_score + "\t\t" + (" " * (max_length - len(player1_score)))
            players2_scores += player2_score + "\t\t" + (" " * (max_length - len(player2_score)))

        print("\n")
        print(players1)
        print(players2)
        print(players1_scores)
        print(players2_scores)
        print("\n")

    def print_list_match2(self, list_match):
        turn_list_match = []
        for match in list_match:
            match_serialized = match.serialize()
            match_serialized['player1'] = match.player1.first_name + " " + match.player1.last_name
            match_serialized['player2'] = match.player2.first_name + " " + match.player2.last_name
            turn_list_match.append(match_serialized)
        df = pd.DataFrame(turn_list_match)
        table = df.loc[:, ~df.columns.isin(['player1_score', 'player2_score'])]
        final_table = table.reset_index(drop=True)
        print("Liste des matchs du round")
        print(final_table)
        input("appuyer sur entrée pour continuer")

    def print_ranking(self, list_player):
        list_player_serialized = []
        for player, score in list_player:
            player_serialized = player.serialize()
            player_serialized["score"] = score
            list_player_serialized.append(player_serialized)
        df = pd.DataFrame(list_player_serialized)
        table = df.loc[:, ~df.columns.isin(['already_met', 'id'])].sort_values(by=['last_name'])
        final_table = table.reset_index(drop=True)
        print("Liste des joueurs inscrit au tournoi")
        print(final_table)
        input("appuyer sur entrée pour continuer")

    def print_ongoing_tournament(self, list_ongoing_tournament):
        i = 1
        for tournament in list_ongoing_tournament:
            print("[" + str(i) + "]" + str(tournament["name"]))
            i += 1

    def get_tournament_indice(self, tournament_length):
        label = "Veuillez entrer le nombre correspondant au tournoi: "
        choice = ic.check_number_input(label)
        if int(tournament_length) >= choice > 0:
            return choice
        else:
            print("Veuillez entrer un chiffre entre 1 et " + str(tournament_length))
            return self.get_tournament_indice(tournament_length)

    def print_tournament_list(self, tournaments):
        df = pd.DataFrame(tournaments)
        print(df)
        input("appuyer sur entrée pour continuer")

    def tournament_error(self, error_code):
        match error_code:
            case TournamentManager.NO_PLAYER_ERROR:
                print("Pas de joueurs inscrits")
            case TournamentManager.NOT_ENOUGH_PLAYERS:
                print("Pas assez de joueurs inscrits")
            case TournamentManager.MAX_PLAYERS_ERROR:
                print("Nombre de joueurs max atteint")
            case TournamentManager.NO_TOURNAMENT_CREATED:
                print("Pas de tournoi crée")
            case TournamentManager.MAX_ROUND_ERROR:
                print("Limite de round atteinte")
        input("appuyer sur entrée pour continuer")

    def print_tournament_created(self):
        print("Tournoi crée")
