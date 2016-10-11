from scraper import *

scraper = Scraper()
team = Team('Creteil II', 'Nationale IV', 'Groupe V')
scraper.scrape_team('http://www.echecs.asso.fr/ListeJoueurs.aspx?Action=EQUIPE&Equipe=2792', team)
print scraper.players
