
class Menu:
    def print_menu(self):
        print("Menu")
        print()
        print("[1] Créer un tournoi")
        print("[2] Ajouter un joueur")

        choice = input("choix:")
        if int(choice) > 3:
            self.print_menu()

        return choice
