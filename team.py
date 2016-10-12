class Team:
    def __init__(self, name, division, group):
        self.name = name
        self.division = division
        self.group = group
        self.players = []
        self.number_rounds = 0

    def __str__(self):
        value = self.name + ' (' + self.division + ', ' + self.group + ') ' + str(self.number_rounds) + '\n'
        self.players.sort(key=lambda player: player.name)
        for p in self.players:
            value += str(p) + '\n'
        return value

    def add(self, player):
        found = 0
        for p in self.players:
            if p.name == player.name:
                found = 1
                p += player
                break
        if found == 0:
            self.players.append(player)
