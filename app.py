import gi, os, re
gi.require_version('Gtk','3.0')
from tokenize import tokenize, untokenize, NUMBER, STRING, NAME, OP
from gi.repository import Gtk, GLib
from pathlib import Path

BASE_PATH = os.path.dirname(__file__)

class Application(Gtk.Application):

    builder = Gtk.Builder.new_from_file(os.path.join(BASE_PATH,'resources','main.ui'))
    #TODO this needs to be less generic
    with_plus_character = re.compile(r"^[pLcbaA]\s+.*")
    generic_expression = re.compile('\s+([^\s]+)\s+', re.IGNORECASE)


    def __init__(self):
        Gtk.Application.__init__(self,
            application_id="tk.eigh.tmp-manager")

        self.init()
        self.window = None

    def init(self):
        self.tmp_file_path = Path('/etc/tmpfiles.d')

    def do_activate(self):
        if not self.window:
            self.window = self.builder.get_object('main')
            self.window.set_application(self)

        self.window.present()

    def do_startup(self):
        Gtk.Application.do_startup(self)

        print("starting up","opening files as tabs")
        editor = self.builder.get_object("editor")
        for tmpfile in self.tmp_file_path.glob('*.conf'):
            print("need to make tab for file:",tmpfile)
            #TODO check for file, or symlink, but we assume there are no directorys or similar example name ends not with conf
            with tmpfile.open() as f:
                #MNEMOIC we make this fuction handlig the file
                self.parse(f)
                    #INFO we match lines agains regular expressions
                    #with_plus_character= ['p','L','c','b','a','A ']
                    #MNEMOIC we check for with_plus_character first
                    #MNEMOIC first_character_list: 'fFwdDevqQPp+LL+cc+bb+CxXrRzZtThHaa+AA+'

        editor.show_all()

    def parse(self,file):
        print("parsing",file)

#TODO move to Widget folder or something
class TabFromPath(Gtk.Spinner):

    def __init__(self,*args):
        Gtk.Spinner.__init__(self)
