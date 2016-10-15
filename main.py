from scraper import *
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

win = Gtk.Window()
win.set_title('3.7-c-d-e')
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()

scraper = Scraper()
results = scraper.search_club('Cre')
scraper.scrape_club(results[3][3])
for t in scraper.teams:
    print t
