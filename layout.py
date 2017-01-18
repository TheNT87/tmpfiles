# -*- coding UTF-8 -*- #

import gi
gi.require_versions({
    'Gtk': '3.0', 'GLib': '2.0'
})

from gi.repository import Gtk, GLib
from gi_composites import GtkTemplate

# This is only required to make the example with without requiring installation
# - Most of the time, you shouldn't use this hack
import sys
from os.path import join
sys.path.insert(0, join( GLib.get_current_dir(), '..'))


@GtkTemplate(ui='widgets/resources/Titlebar.ui')
class Titlebar(Gtk.HeaderBar):

    __gtype_name__ = 'Titlebar'

    #entry = GtkTemplate.Child()

    def __init__(self):
        super(Gtk.HeaderBar, self).__init__()

        # This must occur *after* you initialize your baseS
        self.init_template()
