__author__ = 'Tanguy ROUFFIGNAC'

import mechanize
from bs4 import BeautifulSoup

br = mechanize.Browser()
br.open('http://www.echecs.asso.fr/ListeJoueurs.aspx?Action=EQUIPE&Equipe=2792')
soup = BeautifulSoup(br.response().read(), 'lxml')
players = soup("tr")
del players[0:2]
for i in range (0, len(players)):
    print players[i]("td")[0].text + ' ' + players[i]("td")[1].text
