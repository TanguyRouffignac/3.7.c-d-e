class Player:
    def __init__(self, name, game_number):
        self.name = name
        self.game_number = game_number

    def __str__(self):
        return str(self.game_number) + ' ' + self.name

    def __add__(self, other):
        self.game_number += other.game_number
