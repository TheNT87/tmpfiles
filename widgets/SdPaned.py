# -*- coding UTF-8 -*- #

import gi
gi.require_versions({
    'Gtk': '3.0', 'GLib': '2.0',
    'Secret':'1', 'Polkit':'1.0'
})

from gi.repository import Gtk, GLib, GObject, Gio, Secret, Gdk, Polkit, cairo
from gi_composites import GtkTemplate
gi.require_foreign("cairo")
# This is only required to make the example with without requiring installation
# - Most of the time, you shouldn't use this hack
import sys, logging, os, re
from os.path import join
sys.path.insert(0, join( GLib.get_current_dir(), '..'))

from pathlib import Path


from contextlib import contextmanager

def draw_files(stack):
    for tmpfile in Path('/etc/tmpfiles.d').glob('*.conf'): #TODO  if tmpfile.is_file()
        uri = tmpfile.absolute().as_uri()
        obj = TmpFiles('*.conf')
        #gfile = Gio.File.new_for_uri(uri)
        widget = SdPanedChild(uri)
        stack.add_titled(widget, tmpfile.name, 'stack-0')
        print("activating tmpfiles",tmpfile)
        widget.show()
    print("realizing",stack)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

class TmpFiles(Gio.Permission):
    """This will be the docstring for TmpFile"""

    __gtype_name__ = "TmpFiles"

    path = GObject.Property(type=str, default='/etc/tmpfiles.d')
    is_authorized_write = GObject.Property(type=bool, default=False)

    def __init__(self,*args, **kwargs):
        """The init method takes a glob as argument"""
        GObject.GObject.__init__(self)

        self.text_buff_map = {}

        self.polkit_authority = Polkit.Authority.get()
        self.polkit_perm = Polkit.Permission.new_sync("org.freedesktop.policykit.exec")

        print(self.list_properties(),self.polkit_perm)


    @GObject.Property
    def admin_path(self):
        """returns glob generator"""
        path = Path(self.props.path)
        if path.is_dir():
            return path.glob('*.conf')

    def check_permission(self):
        """check for the right permision and retrun so or None"""
        as_gfile = lambda path_file : Gio.File.new_for_uri(path_file.absolute().as_uri())

        print("os info:",os.getlogin(),os.getgroups(),self.dummy(self.polkit_authority))
        return None

    def parse(self,pane):
        print("parsing files",self,"for pane:",pane)
        for tmpfile in self.props.admin_path:
            #this aproach is blocking
            tmpfile_simple_name = tmpfile.name.split('.')[0]
            with tmpfile.open() as f:
                curr_buff = []
                for line in f.readlines():
                    if not re.search(r"^#",line):
                        print("parsing line: {} in file:{}".format(line,tmpfile.name))
                        buff = Gtk.TextBuffer.new()
                        buff.set_text(line.rstrip())
                        curr_buff.append(buff)
                self.text_buff_map[tmpfile_simple_name] = curr_buff
            print("gotit: {}".format(self.text_buff_map))
            pane.stack.add_titled(
             Gtk.TextView.new_with_buffer(TmpFileBuffer(tmpfile)),
             tmpfile_simple_name, tmpfile.name
            )
            pane.show_all()

    def dummy(self,*args):
        for arg in args:
            print(dir(arg))
        return "dummy string"


class TmpFileBuffer(Gtk.TextBuffer):
    """This class holds a reference to the file it belongs to in a tag"""

    __gtype_name__ = "TmpFileBuffer"

    def __init__(self, tmpfile):
        super(TmpFileBuffer, self).__init__()
        self.create_tag(tmpfile.name)
        self.set_text(tmpfile.read_text())


@GtkTemplate(ui='widgets/resources/SdPaned.ui')
class SdPaned(Gtk.Paned):

    __gtype_name__ = 'SdPaned'

    stack = GtkTemplate.Child()

    def __init__(self):
        super(SdPaned, self).__init__()

        # This must occur *after* you initialize your base
        self.init_template()

        self.tmpfiles = TmpFiles()
        self.connect_after("realize",self.tmpfiles.parse)




#class SdPanedChild(Gtk.Label):
#
#    __gtype_name__ = 'SdPanedChild'
#
#    file_attr = Gio.FILE_ATTRIBUTE_ACCESS_CAN_WRITE
#
#    def __init__(self, uri):
#        super(SdPanedChild, self).__init__()
#
#        self.cancellable = Gio.Cancellable()
#
#        self.gfile = Gio.File.new_for_uri(uri)
#        print(self.gfile.query_info(self.file_attr, Gio.FileQueryInfoFlags.NONE).get_attribute_boolean(self. file_attr))
#        self.gfile.read_async(GLib.PRIORITY_DEFAULT_IDLE, self.cancellable, self.on_read_tmpfile, None)
#
#    def on_read_tmpfile(self, obj, res, user_data):
#        try:
#            gfile_in_stream = obj.read_finish(res)
#        except GLib.GError as e:
#            print("Error: " + e.message)
#        else:
#            data = Gio.DataInputStream.new(gfile_in_stream)
#            (line, size) = data.read_line_utf8()
#            self.set_text(line)
#        finally:
#            self.cancellable.reset()
#
