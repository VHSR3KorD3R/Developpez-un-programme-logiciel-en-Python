class Player:
    def __init__(self, first_name, last_name, birthdate, gender, elo, already_met=None):
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate
        self.gender = gender
        self.elo = elo
        self.already_met = already_met if already_met is not None else []

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

    def serialize(self):
        player: dict = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birthdate": self.birthdate,
            "gender": self.gender,
            "elo": self.elo,
            "already_met": self.already_met
        }
        return player

    def deserialize(self, player_serialized):
        deserialized_player = Player(
            first_name=player_serialized["first_name"],
            last_name=player_serialized["last_name"],
            birthdate=player_serialized["birthdate"],
            gender=player_serialized["gender"],
            elo=player_serialized["elo"],
            already_met=player_serialized["already_met"]
        )
        return deserialized_player
