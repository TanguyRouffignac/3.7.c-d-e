import mechanize
from bs4 import BeautifulSoup
from player import *

br = mechanize.Browser()
br.open('http://www.echecs.asso.fr/ListeJoueurs.aspx?Action=EQUIPE&Equipe=2792')
soup = BeautifulSoup(br.response().read(), 'lxml')
players = soup("tr")
del players[0:2]
for i in range(0, len(players)):
    player = Player(players[i]("td")[1].text, int(players[i]("td")[0].text))
    print player
