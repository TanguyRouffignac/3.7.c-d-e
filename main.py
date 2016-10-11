import mechanize
from bs4 import BeautifulSoup
from player import *
from team import *

br = mechanize.Browser()
team = Team('Creteil II', 'Nationale IV', 'Groupe V')
br.open('http://www.echecs.asso.fr/ListeJoueurs.aspx?Action=EQUIPE&Equipe=2792')
soup = BeautifulSoup(br.response().read(), 'lxml')
players = soup("tr")
del players[0:2]
for p in players:
    player = Player(p("td")[1].text, int(p("td")[0].text))
    team.add(player)
for p in players:
    player = Player(p("td")[1].text, int(p("td")[0].text))
    team.add(player)
print team
