#HINT this class handles the configuration

import gi,re
gi.require_version('GObject','2.0')
from gi.repository import GObject

class Parser(GObject.Object):

    def __init__(self,line):
        Gobject.Object.__init__(self)


    @GObject.property
    def modifier(self):
        return self.modifier

    #INFO we match lines agains regular expressions
    #with_plus_character= ['p','L','c','b','a','A ']
    #MNEMOIC we check for with_plus_character first
    #MNEMOIC first_character_list: 'fFwdDevqQPp+LL+cc+bb+CxXrRzZtThHaa+AA+'

a = re.compile(r"""(?P<modifier>\w\+?)
    \s+  # the modifier part
    (?P<path>.*) # the path

    """, re.X)
###
#\s+
#\s(?P<mode>[-\d]+)  # the mode
#\s(?P<uid>[\d\w]+) # UID
#\s(?P<gid>[\d\w]+) # GID
#\s(?P<age>\d+[whdsm]?)
               ###


def split_line(file):
    result = []
    for line in file:
        result = re.split('\s+',line)
    return result
