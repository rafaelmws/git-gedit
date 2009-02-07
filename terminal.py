import gtk
#import gedit
import os
import os.path
from vte import Terminal

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

       # self.term.connect("child-exited", lambda term: term.fork_command('irb'))
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

    def get_branch(self):
        self.git_root = self.get_git_root(self.uri)
        f = open(os.path.join(self.git_root,".git", "HEAD"))
        return f.readlines()[0].split("/")[-1]
    
    def get_all_branchs(self):
        self.git_root = self.get_git_root(self.uri)
        diretorios = os.listdir(os.path.join(self.git_root,".git", "refs", "heads"))
        return diretorios
        
    
    def run(self,command=''):
        self.git_root = self.get_git_root(self.uri)
    
        if self.git_root=='':
            os.popen("notify-send -t 1600 -i gtk-dialog-info 'Alert!' 'Open a git project file before'")
        elif command.strip()=='':
            os.popen("notify-send -t 1600 -i gtk-dialog-info 'Alert!' 'Hey, type something!'")
        else:    
            self.git_root = self.get_git_root(self.uri)
            self.term.feed_child("cd "+self.git_root+" \n")
            self.term.feed_child(command+"\n")

            self.bottom.show()

            self.image = gtk.Image()
            self.image.set_from_icon_name('gnome-mime-application-x-shellscript', gtk.ICON_SIZE_MENU)

            self.bottom.add_item(self.container, _('Run Git Command: '+command), self.image)
            self.bottom.activate_item(self.container)
            self.term.grab_focus()

    def get_git_root(self, uri):
        base_dir = os.path.dirname(uri)
        depth = 10
        git_root = ''
        while depth > 0:
            depth -= 1
            app_dir = os.path.join(base_dir, '.git')
            if os.path.isdir(app_dir):
                git_root = base_dir
                break
            else:
                base_dir = os.path.abspath(os.path.join(base_dir, '..'))

        return git_root
