import pandas as pd

from Controller import InputChecker as ic
from tabulate import tabulate
from tinydb import Query
from Controller import db

class Menu:

    def print_menu(self):
        print("Menu Tournoi")
        print()
        print("[1] Créer un tournoi")
        print("[2] Reprendre un tournoi")
        print("[3] Créer un joueur")
        print("[4] Afficher les joueurs")
        print("[5] Afficher les tournois")
        print("[6] Rapports")

        choice = ic.check_number_input("choix: ")
        if int(choice) > 6:
            self.print_menu()
        return choice

    def print_reports(self):
        print("[1] Liste des joueurs")
        print("[2] Liste des tournois")
        print("[3] Chercher un tournoi")
        print("[4] Afficher les informations d'un tournoi")

        choice = ic.check_number_input("choix: ")
        if int(choice) > 4:
            self.print_menu()
        return choice

    def print_list_players(self, list_players):
        table = pd.DataFrame(list_players)
        final_table = table.loc[:, ~table.columns.isin(['already_met', 'id'])].sort_values(by=['last_name'])
        final_table = final_table.reset_index(drop=True)
        print(final_table)

    def print_list_tournament(self, list_tournaments):
        table = pd.DataFrame(list_tournaments)
        table.drop(['list_rounds', 'list_players', 'turns', 'current_turn', 'is_ongoing'], axis=1, inplace=True)
        final_table = table.reset_index(drop=True)
        print(final_table)

    def chose_tournament(self):
        return ic.check_number_input("choix: ")

    def search_tournament(self):
        print("Veuillez entrer un nom de tournoi:")
        name = input()
        return name

    def print_tournament(self, tournament):
        list_rounds = tournament.get('list_rounds')
        table = pd.DataFrame(list_rounds)
        table.drop(['list_match'], axis=1, inplace=True)
        final_table = table.reset_index(drop=True)
        list_match = []
        #print(final_table)
        for round in list_rounds:
            #list_match.append(round.get('list_match'))
            list_match = round.get('list_match')
            table = pd.DataFrame(list_match)
            list_match = table.reset_index(drop=True)
            list_match = list_match[['player1', 'player1_score', 'player2', 'player2_score']]
            player1_ids = list_match.get('player1')
            player2_ids = list_match.get('player2')
            i = 0
            for player1_id in player1_ids:
                player = db.players().get(doc_id=player1_id)
                list_match.at[i, 'player1'] = player.get('last_name')
                i += 1
            i = 0
            for player2_id in player2_ids:
                player = db.players().get(doc_id=player2_id)
                list_match.at[i, 'player2'] = player.get('last_name')
                i += 1
            print(round['name'])
            print(list_match)
            #print(list_match)

