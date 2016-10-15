from scraper import *

scraper = Scraper()
results = scraper.search_club('Cre')
scraper.scrape_club(results[3][3])
for t in scraper.teams:
    print t
