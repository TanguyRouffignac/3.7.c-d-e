from scraper import *
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='3.7-c-d-e', default_width=800, default_height=600)
        self.scraper = Scraper()
        self.set_title('3.7-c-d-e')
        self.connect("delete-event", Gtk.main_quit)
        self.box = Gtk.Box(spacing=5)
        self.entry = Gtk.Entry()
        self.button = Gtk.Button(label='Rechercher')
        self.button.connect("clicked", self.on_button_clicked)
        self.box.pack_start(self.entry, True, True, 0)
        self.box.pack_start(self.button, True, True, 0)
        self.add(self.box)
        self.show_all()
        Gtk.main()

    def on_button_clicked(self, widget):
        results = self.scraper.search_club(self.entry.get_text())
        self.scraper.scrape_club(results[3][3])
        for t in self.scraper.teams:
            print t
