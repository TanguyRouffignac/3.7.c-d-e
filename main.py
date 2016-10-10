__author__ = 'Tanguy ROUFFIGNAC'

import mechanize
from bs4 import BeautifulSoup

br = mechanize.Browser()
br.open('http://www.echecs.asso.fr/ListeJoueurs.aspx?Action=EQUIPE&Equipe=2792')
soup = BeautifulSoup(br.response().read(), 'lxml')
print len(soup("tr")) - 2