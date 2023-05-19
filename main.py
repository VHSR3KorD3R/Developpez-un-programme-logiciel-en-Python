from Controller import TournamentManager as tm
from View import Menu as me

NUMBER_OF_ROUNDS = 4

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    menu_view = me.Menu()
    tournament = tm.TournamentManager(menu_view)
    tournament.run()
