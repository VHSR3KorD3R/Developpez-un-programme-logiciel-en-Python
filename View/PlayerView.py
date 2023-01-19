from Controller import InputChecker as ic


class PlayerView:
    def create_player_menu(self):
        first_name = ic.check_user_input("Prénom du joueur")
        last_name = ic.check_user_input("Nom du joueur")
        birthdate = ic.check_date_input("Date de naissance")
        elo = ic.check_number_input("Classement du joueur")
        return {
            "first_name": first_name,
            "last_name": last_name,
            "birthdate": birthdate,
            "elo": elo}

    def search_for_player(self):
        print("chercher un joueur en base avec son nom")
        return input("Nom du joueur")

    def player_not_found(self):
        print("Joueur non trouvé")
        return ic.check_yes_no_input("Voulez-vous en créer un? O: Oui N: Non")
