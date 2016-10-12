import mechanize
from bs4 import BeautifulSoup
from player import *
from team import *
import re

titles = ['g', 'm', 'f', 'gf', 'mf', 'ff']
leagues = [["Ligue de l'Ile de France", ["Essonne 1", "Hauts de Seine 1", "Paris 1", "Seine et Marne 1",
                                         "Seine Saint Denis 1", "Val de Marne 1", "Val d'Oise 1", "Yvelines 1"]]]


class Scraper:
    def __init__(self):
        self.browser = mechanize.Browser()
        self.teams = []
        self.players = Team('', '', '')

    def scrape_team(self, url, team):
        self.browser.open('http://www.echecs.asso.fr/' + url)
        soup = BeautifulSoup(self.browser.response().read(), 'lxml')
        matches = soup.body.find_all("div", class_="page-mid")[0].td
        rounds = matches.find_all("a", class_="lien_titre")
        for r in rounds:
            self.browser.form = list(self.browser.forms())[-1]
            self.browser.form.new_control('hidden', '__EVENTTARGET', {'value': r['id'].replace('_', '$')})
            self.browser.form.new_control('hidden', '__EVENTARGUMENT', {'value': ''})
            self.browser.form.new_control('hidden', '__LASTFOCUS', {'value': ''})
            self.browser.submit()
            soup = BeautifulSoup(self.browser.response().read(), 'lxml')
            matches = soup.body.find_all("div", class_="page-mid")[0].td
            matches = matches("tr")
            del matches[0]
            number_matches = 0
            for line in matches:
                if line['class'][0] == "tableau_magenta":
                    number_matches += 1
            number_boards = len(matches) / number_matches - 1
            for i in range(0, number_matches):
                color = 3
                if matches[i * (number_boards + 1)]("td")[0].text == team.name:
                    color = 0
                if matches[i * (number_boards + 1)]("td")[2].text == team.name:
                    color = 2
                if color < 3:
                    for j in range(0, number_boards):
                        game = matches[i * (number_boards + 1) + j + 1]
                        name = game("td")[color].text
                        if name != '':
                            name = re.split('  ', name)[0]
                            if re.split(' ', name)[0] in titles:
                                words = re.split(' ', name)
                                name = ''
                                del words[0]
                                for word in words[0:len(words) - 1]:
                                    name += word + ' '
                                name += words[len(words) - 1]
                            team.add(Player(name, 1))
                    break
            self.browser.form = list(self.browser.forms())[-1]
            self.browser.form.new_control('hidden', '__EVENTTARGET', {'value': ''})
            self.browser.form.new_control('hidden', '__EVENTARGUMENT', {'value': ''})
            self.browser.form.new_control('hidden', '__LASTFOCUS', {'value': ''})
            self.browser.submit()
        self.teams.append(team)

    def scrape_club(self, url):
        self.browser.open(url)
        soup = BeautifulSoup(self.browser.response().read(), 'lxml')
        teams = soup("tr")
        del teams[0]
        del teams[-1]
        for t in teams:
            if t("td")[1].text == 'Interclubs Adultes':
                team = Team(t("td")[0].text, t("td")[1].text, t("td")[2].text)
                self.scrape_team(t("td")[3]("a")[0]['href'], team)
            if re.split(' ', t("td")[1].text)[0] == 'Ligue':
                for league in leagues:
                    if league[0] == t("td")[1].text:
                        for division in league[1]:
                            if division == t("td")[2].text:
                                team = Team(t("td")[0].text, t("td")[1].text, t("td")[2].text)
                                self.scrape_team(t("td")[3]("a")[0]['href'], team)
