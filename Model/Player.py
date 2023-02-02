class Player:
    def __init__(self, first_name, last_name, birthdate, elo):
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate
        self.elo = elo
        self.already_met = []

    def __str__(self):
        return f"first_name : {self.first_name}\n" \
               f"last_name: {self.last_name}\n" \
               f"birthdate: {self.birthdate}\n" \
               f"elo : {self.elo}\n"

    def __eq__(self, other):
        if isinstance(other, Player):
            return self.first_name == other.first_name and \
                   self.last_name == other.last_name and \
                   self.birthdate == other.birthdate
        return NotImplemented
