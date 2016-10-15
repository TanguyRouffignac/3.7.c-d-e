from scraper import *
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='3.7-c-d-e', default_width=800, default_height=600)
        self.scraper = Scraper()
        self.set_title('3.7-c-d-e')
        self.connect("delete-event", Gtk.main_quit)
        self.box = Gtk.Box(spacing=5)
        self.entry = Gtk.Entry()
        self.entry.connect("key-press-event", self.key_press)
        self.button = Gtk.Button(label='Rechercher')
        self.button.connect("clicked", self.on_search_launched)
        self.box.pack_start(self.entry, True, True, 0)
        self.box.pack_start(self.button, True, True, 0)
        self.add(self.box)
        self.show_all()
        Gtk.main()

    def key_press(self, widget, event):
        if event.keyval == Gdk.KEY_Return:
            results = self.scraper.search_club(self.entry.get_text())
            self.remove(self.box)
            self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            for r in results:
                b = Gtk.Button(label=r[2])
                b.connect("clicked", self.on_club_clicked)
                b.href = r[3]
                self.box.pack_start(b, True, True, 0)
            self.add(self.box)
            self.show_all()

    def on_search_launched(self, widget):
        results = self.scraper.search_club(self.entry.get_text())
        self.remove(self.box)
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        for r in results:
            b = Gtk.Button(label=r[2])
            b.connect("clicked", self.on_club_clicked)
            b.href = r[3]
            self.box.pack_start(b, True, True, 0)
        self.add(self.box)
        self.show_all()

    def on_club_clicked(self, widget):
        self.remove(self.box)
        while Gtk.events_pending():
            Gtk.main_iteration_do(False)
        self.scraper.scrape_club(widget.href)
        for t in self.scraper.teams:
            print t
