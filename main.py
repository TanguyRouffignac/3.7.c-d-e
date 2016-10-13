from scraper import *

scraper = Scraper()
scraper.scrape_club('http://www.echecs.asso.fr/ListeEquipes.aspx?ClubRef=84')
for t in scraper.teams:
    print t
