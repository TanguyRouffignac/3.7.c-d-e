class Player:
    def __init__(self, name, game_number):
        self.name = name
        self.game_number = game_number

    def __str__(self):
        return str(self.game_number) + ' ' + self.name

    def add_games(self, number):
        self.game_number += number
