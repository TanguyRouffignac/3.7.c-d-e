from scraper import *

scraper = Scraper()
scraper.search_club('Cre')
for t in scraper.teams:
    print t
