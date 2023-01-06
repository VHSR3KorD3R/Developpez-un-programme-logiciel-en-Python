import random
from Controller import PlayerManager as pm, RoundManager as rm, TournamentManager as tm

NUMBER_OF_ROUNDS = 4

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    tournament = tm.TournamentManager()
    tournament.create_tournament("tournament",
                                 "Paris",
                                 "01/01/1970",
                                 NUMBER_OF_ROUNDS,
                                 "bullet",
                                 "description")

    for match in tournament.list_rounds[0].list_match:
        results = random.choice([0, 0.5, 1])
        if results == 0:
            match.player1_score = 0
            match.player2_score = 1
            tournament.update_player_score(match.player2, 1)
        if results == 1:
            match.player1_score = 1
            tournament.update_player_score(match.player1, 1)
            match.player2_score = 0
        if results == 0.5:
            match.player1_score = 0.5
            tournament.update_player_score(match.player1, 0.5)
            match.player2_score = 0.5
            tournament.update_player_score(match.player2, 0.5)

    for i in range(1, NUMBER_OF_ROUNDS):
        tournament.create_rounds("rounds " + str(i), "01/01/1970")
        for match in tournament.list_rounds[i].list_match:
            results = random.choice([0, 0.5, 1])
            if results == 0:
                match.player1_score = 0
                match.player2_score = 1
                tournament.update_player_score(match.player2, 1)
            if results == 1:
                match.player1_score = 1
                tournament.update_player_score(match.player1, 1)
                match.player2_score = 0
            if results == 0.5:
                match.player1_score = 0.5
                tournament.update_player_score(match.player1, 0.5)
                match.player2_score = 0.5
                tournament.update_player_score(match.player2, 0.5)

    tournament.list_players.sort(key=lambda x: x[1])

    for i in tournament.list_players:
        print(i[0])
        print("score: " + str(i[1]))

    print(tournament.list_players)


