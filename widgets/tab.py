import gi, os, re
gi.require_version('Gtk','3.0')
from tokenize import tokenize, untokenize, NUMBER, STRING, NAME, OP
from gi.repository import Gtk, GLib
from pathlib import Path
from conf import split_line

#TODO move to Widget folder or something
class TabWidget(Gtk.Notebook):

    __gtype_name__ = "TabWidget"
    tmp_file_path = Path('/etc/tmpfiles.d')

    def __init__(self,*args):
        super(TabWidget, self).__init__()
        for tmpfile in self.tmp_file_path.glob('*.conf'):
            print("need to make tab for file:",tmpfile)
            #TODO check for file, or symlink, but we assume there are no directorys or similar example name ends not with conf
            self.append_page(ManipulatorBox(tmpfile),Gtk.Label.new(tmpfile.name))

        self.show_all()

    def parse(self,line):
        items = re.split('\s+',line)

class ManipulatorBox(Gtk.ListBox):

    __gtype_name__ = "ManipulatorBox"
    #MAYBE constructor args are settable as properties Gtk.Orientation.HORIZONTAL,2

    def __init__(self,*args):
        super(ManipulatorBox, self).__init__()

        for line in args[0].open():
            if not re.search("^#",line):
                gstring = GLib.utf8_normalize(line.rstrip(),-1,GLib.NormalizeMode.DEFAULT)
                buff = Gtk.EntryBuffer.new(gstring,-1)
                self.add(Gtk.Entry.new_with_buffer(buff))

    def do_show(self):
        Gtk.ListBox.do_show(self)
        print("manpulator showing")

#with tmpfile.open() as f:
    #MNEMOIC we make this fuction handlig the file
    #for line in f:
        #if not re.match('#.*',line):
            #TabFromPath(line)
