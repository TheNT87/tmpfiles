import gi, os, re
gi.require_versions({
    'Gtk':'3.0', 'Secret': '1'
})
from tokenize import tokenize, untokenize, NUMBER, STRING, NAME, OP
from gi.repository import Gtk, GLib, GObject, Secret

import layout
from widgets.SdPaned import *

BASE_PATH = os.path.dirname(__file__)

class Application(Gtk.Application):

    __gtype_name__ = 'GtkSdManager'
    #TODO change to repository from gresouce

    def __init__(self):
        super(Application, self).__init__(application_id="tk.eigh.tmp-manager",register_session=True)
        self.builder = Gtk.Builder.new_from_file(os.path.join(BASE_PATH,'resources','main.ui'))

        self.window = None

    def on_activate(self,app):
        print("activation app",app)
        if not self.window:
            self.window = self.builder.get_object('main')
            self.window.set_application(app)
            self.window.set_titlebar(layout.Titlebar())
            self.window.set_default_size(200, 200)

        self.window.present()

    def do_startup(self):
        Gtk.Application.do_startup(self)

        print("starting up","opening files as tabs")
        main_box = self.builder.get_object("main-box")
        main_box.add(SdPaned())
        main_box.show_all()

    def do_dbus_register(self, conn, path):
        self.secrets = Secret.Service.get_sync(Secret.ServiceFlags.LOAD_COLLECTIONS)#OPEN_SESSION)
        return True

    def run(self, argv):
        self.connect('activate', self.on_activate)
        return super(Application, self).run(argv)
