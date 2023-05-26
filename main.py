from Controller import TournamentManager as tm
from View import Menu as me

if __name__ == '__main__':

    menu_view = me.Menu()
    tournament = tm.TournamentManager(menu_view)
    tournament.run()
