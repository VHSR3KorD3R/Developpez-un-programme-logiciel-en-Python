from Controller import InputChecker as ic

import pandas as pd


class PlayerView:
    def create_player_menu(self):
        first_name = ic.check_user_input("Prénom du joueur: ")
        last_name = ic.check_user_input("Nom du joueur: ")
        birthdate = ic.check_date_input("Date de naissance: ")
        gender = ic.check_user_input("Genre du joueur: ")
        elo = ic.check_number_input("Classement du joueur: ")
        return {
            "first_name": first_name,
            "last_name": last_name,
            "birthdate": birthdate.strftime("%d/%m/%Y"),
            "gender": gender,
            "elo": elo}

    def search_for_player(self):
        print("chercher un joueur en base avec son nom")
        return input("Nom du joueur: ")

    def player_not_found(self):
        print("Joueur non trouvé")
        return ic.check_yes_no_input("Voulez-vous en créer un? O: Oui N: Non ")

    def print_list_players(self, list_players):
        i = 1
        for player in list_players:
            print("[" + str(i) + "]" + str(player))
            i += 1

    def get_player_indice(self):
        label = "Veuillez entrer le nombre correspondant au joueur à inscrire: "
        return ic.check_number_input(label)

    def print_already_exists_player(self):
        print()
        print("Le joueur est déja inscrit au tournoi")
        print()

    def print_list_player(self, players):
        table = pd.DataFrame(players)
        final_table = table.loc[:, ~table.columns.isin(['already_met', 'id'])].sort_values(by=['last_name'])
        final_table = final_table.reset_index(drop=True)
        print(final_table)

    def print_error(self):
        print("Pas de joueurs crée")

    def print_player_created(self):
        print("Joueur crée")

    def print_player_added(self):
        print("Joueur ajouté au tournoi")
