
class Round:
    def __init__(self, name, start_time):
        self.name = name
        self.start_time = start_time
        self.end_time = None
        self.list_match = []

    def __str__(self):
        return f"round_name : {self.name}\n" \
               f"start_time: {self.start_time}\n" \
               f"list_match : {self.list_match}\n"
