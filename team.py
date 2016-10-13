class Team:
    def __init__(self, name, division, group):
        self.name = name
        self.division = division
        self.group = group
        self.players = []
        self.number_rounds = 0
        self.unavailable_players = []

    def __str__(self):
        value = self.name + ' (' + self.division + ', ' + self.group + ') ' + str(self.number_rounds) + '\n'
        self.players.sort(key=lambda player: player.name)
        self.unavailable_players.sort()
        for p in self.players:
            value += str(p) + '\n'
        value += '\nNe peuvent jouer la prochaine ronde :\n'
        for p in self.unavailable_players:
            value += p[0]
            if p[1] == 'c':
                value += ' (3.7.c)\n'
            if p[1] == 'd':
                value += ' (3.7.d)\n'
            if p[1] == 'e':
                value += ' (3.7.e)\n'
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
