class PlayerView:
    def create_player_menu(self):
        first_name = input("Prénom du joueur")
        last_name = input("Nom du joueur")
        birthdate = input("Date de naissance")
        elo = int(input("Classement du joueur"))
        return {
            "first_name": first_name,
            "last_name": last_name,
            "birthdate": birthdate,
            "elo": elo}