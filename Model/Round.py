from Model import Match as ma


class Round:
    def __init__(self, name, start_time, end_time=None, list_match=None):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.list_match = list_match

    def __str__(self):
        return f"round_name : {self.name}\n" \
               f"start_time: {self.start_time}\n"
        # f"list_match : {self.list_match}\n"

    def serialize(self):
        serialized_list_match = []
        for match in self.list_match:
            serialized_list_match.append(match.serialize())
        round: dict = {
            "name": self.name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "list_match": serialized_list_match
        }
        return round

    @staticmethod
    def deserialize(serialized_round):
        list_match = []
        for serialized_match in serialized_round["list_match"]:
            list_match.append(ma.Match.deserialize(serialized_match))

        deserialized_round = Round(
            name=serialized_round["name"],
            start_time=serialized_round["start_time"],
            end_time=serialized_round["end_time"],
            list_match=list_match
        )
        return deserialized_round
