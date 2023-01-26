from Controller import InputChecker as ic
from datetime import date as da

import os


class TournamentView:
    def create_tournament_menu(self):
        # restructurer les checks dans une autre classe à part
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
        os.system('cls')
        print("[1] créer un joueur")
        print("[2] chercher un joueur")
        print("[3] afficher la liste des inscris au tournoi")
        print("[4] créer un round")
        print("[5] sortir")

        return ic.check_number_input("choix: ")
