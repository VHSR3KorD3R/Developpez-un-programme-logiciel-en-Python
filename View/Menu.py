import os
from Controller import InputChecker as ic


class Menu:

    def print_menu(self):
        print("Menu")
        print()
        print("[1] Créer un tournoi")
        print("[2] Reprendre un tournoi")
        print("[3] Créer un joueur")
        print("[4] Afficher les joueurs")
        print("[5] Afficher les tournois")

        choice = ic.check_number_input("choix: ")
        if int(choice) > 5:
            os.system('cls')
            self.print_menu()
        return choice
