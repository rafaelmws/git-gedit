import gtk
import gedit
import os
import os.path
from vte import Terminal
from githelper import GitHelper

class GitTerminalWidget():
    def __init__(self, window):
        self.window = window
        
        self.bottom = window.get_bottom_panel()
        
        self.uri = window.get_active_document().get_uri_for_display()
        self.term = Terminal()
        self.term.set_emulation("xterm")
        self.term.set_audible_bell(False)
        self.term.set_scrollback_lines(150)
        self.term.set_size_request(10,100)
        self.term.fork_command('bash')
   
        self.term_scrollbar = gtk.VScrollbar()
        self.term_scrollbar.set_adjustment(self.term.get_adjustment())      

        self.term_box = gtk.HBox()
        self.term_box.pack_start(self.term, True, True, 0)
        self.term_box.pack_end(self.term_scrollbar, False, False, 0)     

        self.close_bt = gtk.Button("Close")
        self.close_bt.connect("clicked", self.close_bt_action, "Exit!")
        
        self.container = gtk.VBox(False)

        self.term.connect("child-exited", self.close_term_action_child_exited)
        
        self.table = gtk.Table(2,1,False)
        self.table.attach(self.term_box,0,1,0,1)
        self.table.attach(self.close_bt,0,1,1,2,gtk.FILL|gtk.SHRINK,gtk.FILL|gtk.SHRINK, 0, 0)
        self.container.pack_start(self.table)
        self.close_bt.show()
        self.table.show()
        self.term_box.show_all()       

    def close_bt_action(self, widget, data=None):
      self.close()

    def close_term_action_child_exited(self, term):
      self.close()

    def close(self):
        self.bottom.remove_item(self.container)
        self.bottom.hide()
        self.container.destroy()
    
    def run(self,command=''):
        githelper = GitHelper()
        self.git_root = githelper.get_git_root(self.uri)    

        if self.git_root=='':
            os.popen("notify-send -t 1600 -i gtk-dialog-info 'Alert!' 'Open a git project file before'")
        elif command.strip()=='':
            os.popen("notify-send -t 1600 -i gtk-dialog-info 'Alert!' 'Hey, type something!'")
        else:    

            self.term.feed_child("cd "+self.git_root+" \n")
            self.term.feed_child(command+"\n")

            self.bottom.show()

            self.image = gtk.Image()
            self.image.set_from_icon_name('gnome-mime-application-x-shellscript', gtk.ICON_SIZE_MENU)

            self.bottom.add_item(self.container, _('Run Git Command: '+command), self.image)
            self.bottom.activate_item(self.container)
            self.term.grab_focus()

    
