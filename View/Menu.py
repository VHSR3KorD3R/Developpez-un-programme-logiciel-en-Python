import os

import pandas as pd

from tinydb import Query

from Controller import InputChecker as ic
from tabulate import tabulate
import pandas

class Menu:

    def print_menu(self):
        print("Menu")
        print()
        print("[1] Créer un tournoi")
        print("[2] Reprendre un tournoi")
        print("[3] Créer un joueur")
        print("[4] Afficher les joueurs")
        print("[5] Afficher les tournois")
        print("[6] Rapports")

        choice = ic.check_number_input("choix: ")
        if int(choice) > 6:
            os.system('cls')
            self.print_menu()
        return choice

    def print_reports(self):
        print("[1] Liste des joueurs")
        print("[2] Liste des tournois")
        print("[3] Chercher un tournoi")
        return ic.check_number_input("choix: ")

    def print_list_players(self, list_players):
        table = pd.DataFrame(list_players)
        final_table = table.loc[:, ~table.columns.isin(['already_met', 'id'])].sort_values(by=['last_name'])
        final_table = final_table.reset_index(drop=True)
        print(final_table)
    def print_list_tournament(self, list_tournaments):
        table = pd.DataFrame(list_tournaments)
        #final_table = table.loc[:, ~table.columns.isin(['list_rounds', 'list_players', 'turns'])].sort_values(by=['name'])
        table.drop(['list_rounds', 'list_players', 'turns', 'current_turn', 'is_ongoing'], axis=1, inplace=True)
        final_table = table.reset_index(drop=True)
        print(final_table)

    def search_tournament(self):
        print("Veuillez entrer un nom de tournoi:")
        name = input()
        return name

    def print_tournament(self, tournament):
        list_rounds = tournament.list_rounds
        for round in list_rounds:
            print(round)
            for match in round.list_match:
                print(match)
