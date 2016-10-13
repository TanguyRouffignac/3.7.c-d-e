class Player:
    def __init__(self, name, number_games):
        self.name = name
        self.number_games = number_games

    def __str__(self):
        return str(self.number_games) + ' ' + self.name

    def __add__(self, other):
        self.number_games += other.number_games
