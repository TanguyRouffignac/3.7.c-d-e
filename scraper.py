import mechanize
from bs4 import BeautifulSoup
from player import *
from team import *
import re


class Scraper:
    def __init__(self):
        self.browser = mechanize.Browser()
        self.teams = []
        self.players = Team('', '', '')

    def scrape_team(self, url, team):
        self.browser.open('http://www.echecs.asso.fr/' + url)
        soup = BeautifulSoup(self.browser.response().read(), 'lxml')
        players = soup("tr")
        del players[0:2]
        for p in players:
            player = Player(p("td")[1].text, int(p("td")[0].text))
            team.add(player)
            self.players.add(player)
        self.teams.append(team)

    def scrape_club(self, url):
        self.browser.open(url)
        soup = BeautifulSoup(self.browser.response().read(), 'lxml')
        teams = soup("tr")
        del teams[0]
        del teams[-1]
        for t in teams:
            if t("td")[1].text == 'Interclubs Adultes' or re.split(' ', t("td")[1].text)[0] == 'Ligue':
                team = Team(t("td")[0].text, t("td")[1].text, t("td")[2].text)
                self.scrape_team(t("td")[0]("a")[0]['href'], team)
