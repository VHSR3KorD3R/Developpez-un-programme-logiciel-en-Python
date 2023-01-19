

class RoundManager:
    def __init__(self):
        self.list_match = []

    def show_round(self):
        for match in self.list_match:
            print(match.match.__str__())
