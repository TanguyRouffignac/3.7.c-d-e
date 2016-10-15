import mechanize
from bs4 import BeautifulSoup
from player import *
from team import *
import re

titles = ['g', 'm', 'f', 'gf', 'mf', 'ff']
leagues = [["Ligue d'Alsace", ["Bas Rhin 1", "Haut Rhin 1", "Bas Rhin 2", "Haut Rhin 2", "Bas Rhin 3", "Haut Rhin 3"]],
           ["Ligue d'Aquitaine", ["Aquitaine 1"]],
           ["Ligue de Basse Normandie", ["Basse Normandie 1"]],
           ["Ligue de Bourgogne", ["Bourgogne 1"], ["Bourgogne 2"]],
           ["Ligue de Bretagne", ["Departementales Adultes"]],
           ["Ligue du Centre Val de Loire", ["Centre Val de Loire 1", "Centre Val de Loire 2",
                                             "Promotion 37 Avenir", "Promotion 37 Espoir"]],
           ["Ligue de Champagne Ardenne", ["Champagne Ardenne 1"]],
           ["Ligue de Cote d'Azur", ["Cote d'Azur 1", "Var 1", "Var 2"]],
           ["Ligue du Dauphine Savoie", ["Dauphine Savoie"]],
           ["Ligue de Franche Comte", ["Franche Comte 1"]],
           ["Ligue de Haute Normandie", ["Haute Normandie 1", "Haute Normandie 2"]],
           ["Ligue de l'Ile de France", ["Essonne 1", "Hauts de Seine 1", "Paris 1", "Seine et Marne 1",
                                         "Seine Saint Denis 1", "Val de Marne 1", "Val d'Oise 1", "Yvelines 1"]],
           ["Ligue du Languedoc Roussillon", ["Languedoc Roussillon 1", "Pays Cathare 1"]],
           ["Ligue de Lorraine", ["Lorraine 1", "Lorraine 2"]],
           ["Ligue du Lyonnais", ["Lyonnais 1"]],
           ["Ligue de Midi Pyrenees", ["Midi Pyrenees 1", "Midi Pyrenees 2"]],
           ["Ligue du Nord Pas de Calais", ["Pre Nationale H.D.F.", "Regionale H.D.F.", "Pre Regionale H.D.F."]],
           ["Ligue des Pays de la Loire", ["Loire Atlantique 1", "Loire Atlantique 2", "Maine et Loire 1",
                                           "Mayenne 1", "Pays de la Loire 1", "Sarthe 1", "Vendee 1"]],
           ["Ligue de Picardie", ["Pre Nationale H.D.F.", "Regionale H.D.F."]],
           ["Ligue du Poitou-Charentes", ["Poitou Charentes 1", "Poitou Charentes 2"]],
           ["Ligue de Provence", ["Provence", "Bouches du Rhone 1"]]]


class Scraper:
    def __init__(self):
        self.browser = mechanize.Browser()
        self.browser.open('http://www.echecs.asso.fr')
        self.teams = []
        self.players = Team('', '', '')

    def scrape_team(self, url, team):
        for p in self.players.players:
            if p.number_games >= 3:
                team.unavailable_players.append([p.name, 'c'])
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
                    played = 0
                    for j in range(0, number_boards):
                        game = matches[i * (number_boards + 1) + j + 1]
                        name = game("td")[color].text
                        if name != '':
                            played = 1
                            name = re.split('  ', name)[0]
                            if re.split(' ', name)[0] in titles:
                                words = re.split(' ', name)
                                name = ''
                                del words[0]
                                for word in words[0:len(words) - 1]:
                                    name += word + ' '
                                name += words[len(words) - 1]
                            team.add(Player(name, 1))
                            self.players.add(Player(name, 1))
                    if played:
                        team.number_rounds += 1
                    break
            self.browser.form = list(self.browser.forms())[-1]
            self.browser.form.new_control('hidden', '__EVENTTARGET', {'value': ''})
            self.browser.form.new_control('hidden', '__EVENTARGUMENT', {'value': ''})
            self.browser.form.new_control('hidden', '__LASTFOCUS', {'value': ''})
            self.browser.submit()
        self.teams.append(team)

    def scrape_club(self, url):
        self.browser.open(url)
        self.teams = []
        self.players = Team('', '', '')
        soup = BeautifulSoup(self.browser.response().read(), 'lxml')
        teams = soup("tr")
        del teams[0]
        del teams[-1]
        for t in teams:
            if t("td")[1].text == 'Interclubs Adultes' and t("td")[2].text != "Top 12":
                team = Team(t("td")[0].text, t("td")[2].text, t("td")[3].text)
                self.scrape_team(t("td")[3]("a")[0]['href'], team)
            if re.split(' ', t("td")[1].text)[0] == 'Ligue':
                for league in leagues:
                    if league[0] == t("td")[1].text:
                        for division in league[1]:
                            if division == t("td")[2].text:
                                team = Team(t("td")[0].text, t("td")[2].text, t("td")[3].text)
                                self.scrape_team(t("td")[3]("a")[0]['href'], team)
        for team in self.teams:
            for other in self.teams:
                if team.name != other.name and team.division == other.division:
                    for player in other.players:
                        found = 0
                        for unavailable in team.unavailable_players:
                            if player.name == unavailable[0]:
                                found = 1
                                unavailable[1] = 'd'
                                break
                        if found == 0:
                            team.unavailable_players.append([player.name, 'd'])
            for player in self.players.players:
                if player.number_games > team.number_rounds:
                    found = 0
                    for unavailable in team.unavailable_players:
                        if player.name == unavailable[0]:
                            found = 1
                            break
                    if found == 0:
                        team.unavailable_players.append([player.name, 'e'])

    def search_club(self, name):
        self.browser.select_form('FormClub')
        self.browser.form['ClubNom'] = name
        self.browser.submit()
        soup = BeautifulSoup(self.browser.response().read(), 'lxml')
        clubs = soup("tr")
        del clubs[0:2]
        del clubs[-1]
        result = []
        for c in clubs:
            result.append([c("td")[0].text, c("td")[1].text, c("td")[2].text,
                           'http://www.echecs.asso.fr/' +
                           c("td")[2]("a")[0]['href'].replace('FicheClub.aspx?', 'ListeEquipes.aspx?Club')])
        return result
