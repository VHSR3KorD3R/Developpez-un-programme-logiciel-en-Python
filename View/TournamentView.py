from Controller import InputChecker as ic
from datetime import date as da

import os


class TournamentView:
    def create_tournament_menu(self):
        name = ic.check_user_input("Nom du tournoi: ")
        location = ic.check_user_input("Lieu du tournoi: ")
        today = da.today()
        date = today.strftime("%d/%m/%Y")
        turns = ic.check_number_input("nombre de rounds: ")
        time = ic.check_user_input("Controle du temps: ")
        description = ic.check_user_input("Description: ")
        return {"name": name,
                "location": location,
                "date": date,
                "turns": turns,
                "time": time,
                "description": description
                }

    def print_tournament_menu(self):
        print("[1] créer un joueur")
        print("[2] chercher un joueur")
        print("[3] afficher la liste des inscris au tournoi")
        print("[4] créer un round")
        print("[5] saisir les résultats du round en cours")
        print("[6] voir le classment")
        print("[0] sortir")

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

    def print_ranking(self, list_player):
        for player in list_player:
            print(player[0])
            print("score: " + str(player[1]))

    def print_ongoing_tournament(self, list_ongoing_tournament):
        i = 1
        for tournament in list_ongoing_tournament:
            print("[" + str(i) + "]" + str(tournament["name"]))
            i += 1

    def get_tournament_indice(self):
        label = "Veuillez entrer le nombre correspondant au tournoi"
        return ic.check_number_input(label)

