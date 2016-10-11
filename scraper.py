import mechanize
from bs4 import BeautifulSoup
from player import *
from team import *


class Scraper:
    def __init__(self):
        self.browser = mechanize.Browser()
        self.teams = []
        self.players = Team('', '', '')

    def scrape_team(self, url, team):
        self.browser.open(url)
        soup = BeautifulSoup(self.browser.response().read(), 'lxml')
        players = soup("tr")
        del players[0:2]
        for p in players:
            player = Player(p("td")[1].text, int(p("td")[0].text))
            team.add(player)
            self.players.add(player)
        self.teams.append(team)
