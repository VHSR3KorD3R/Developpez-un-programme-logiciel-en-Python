import os
from Controller import InputChecker as ic

class Menu:

    def print_menu(self):
        print("Menu")
        print()
        print("[1] Créer un tournoi")
        print("[2] Créer un joueur")
        print("[3] Afficher les joueurs")
        print("[4] Afficher les tournois")

        choice = ic.check_number_input("choix: ")
        if int(choice) > 5:
            os.system('cls')
            self.print_menu()
        return choice

