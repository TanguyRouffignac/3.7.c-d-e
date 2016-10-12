class Team:
    def __init__(self, name, division, group):
        self.name = name
        self.division = division
        self.group = group
        self.players = []

    def __str__(self):
        value = self.name + ' (' + self.division + ', ' + self.group + ')'
        self.players.sort(key=lambda player: player.name)
        for p in self.players:
            value += '\n' + str(p)
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
