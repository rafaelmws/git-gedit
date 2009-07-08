import gtk
import gedit
import vte
import os
import os.path
import gtk.glade
import gconf
from gettext import gettext as _
from terminal import GitTerminalWidget
from githelper import GitHelper

ui_str = """
<ui>
    <menubar name="MenuBar">
        <menu name="ViewMenu" action="View">
            <menuitem name="Git Hot Commands" action="GitHotcommands"/>
        </menu>
    </menubar>
</ui>
"""
all_commands_list = {'git add': 'Add file contents to the index',
 'git bisect': 'Find the change that introduced a bug by binary search',
 'git branch': 'List, create, or delete branches',
 'git checkout': 'Checkout a branch or paths to the working tree',
 'git clone ': 'Clone a repository into a new directory',
 'git commit -a -m ': 'Record changes to the repository',
 'git diff': 'Show changes between commits, commit and working tree, etc',
 'git fetch': 'Download objects and refs from another repository',
 'git grep': 'Print lines matching a pattern',
 'git init': 'Create an empty git repository or reinitialize an existing one',
 'git log': 'Show commit logs',
 'git merge': 'Join two or more development histories together',
 'git mv': 'Move or rename a file, a directory, or a symlink',
 'git pull': 'Fetch from and merge with another repository or a local branch',
 'git push': 'Update remote refs along with associated objects',
 'git rebase': 'Forward-port local commits to the updated upstream head',
 'git reset': 'Reset current HEAD to the specified state',
 'git rm': 'Remove files from the working tree and from the index',
 'git show': 'Show various types of objects',
 'git status': 'Show the working tree status',
 'git tag': 'Create, list, delete or verify a tag object signed with GPG'}

GLADE_FILE = os.path.join(os.path.dirname(__file__), "commandrunner.glade")

class GitHotcommandsPlugin(gedit.Plugin):
    def __init__(self):
        gedit.Plugin.__init__(self)
        self.githelper = GitHelper()
        print "Iniciando o plugin Git-Gedit"

    def activate(self, window):
        self.window = window
        self.dialog = None
        self.bottom = window.get_bottom_panel()

        self.mount_list()
        actions = [
            ('GitHotcommands', gtk.STOCK_SELECT_COLOR, _('Git Hot Commands'), 
            '<Control><Alt>g', _("Press Ctrl+Alt+g to run commands"), self.on_open)
        ]

        action_group = gtk.ActionGroup("GitHotcommandsActions")
        action_group.add_actions(actions, self.window)

        self.manager = self.window.get_ui_manager()
        self.manager.insert_action_group(action_group, -1)
        self.manager.add_ui_from_string(ui_str)

    def run_command(self,command):
        term = GitTerminalWidget(self.window)
        term.run(command)

    def on_open(self, *args):
        glade_xml = gtk.glade.XML(GLADE_FILE)

        if self.dialog:
            self.dialog.set_focus(True)
            return

        self.dialog = glade_xml.get_widget('gitcommandrunner_dialog')
        self.dialog.connect('delete_event', self.on_close)
        self.dialog.show_all()
        self.dialog.set_transient_for(self.window)

        self.combo = glade_xml.get_widget('command_list')
        self.combo_branchs = glade_xml.get_widget('branchs_list')
        
        self.mount_branchs_list()
        
        self.description = glade_xml.get_widget('label-description')
        self.branch_label = glade_xml.get_widget('branch_label')
        
        self.cancel_button = glade_xml.get_widget('cancel_button')
        self.cancel_button.connect('clicked', self.on_cancel)

        self.apply_button = glade_xml.get_widget('run_button')
        self.apply_button.connect('clicked', self.on_run)

        self.branch_button = glade_xml.get_widget('branch_button')
        self.branch_button.connect('clicked', self.on_change_branch)

        self.combo.set_model(self.model)
        self.combo.set_text_column(0)
        self.combo.connect('event-after',self.on_change)

        self.combo_branchs.set_model(self.model_branchs)
        self.combo_branchs.set_text_column(0)

        self.completion = gtk.EntryCompletion()
        self.completion.connect('match-selected', self.on_selected)
        
        self.completion.set_model(self.model)
        self.completion.set_text_column(0)

        self.entry = self.combo.get_children()[0]
        self.entry.set_completion(self.completion)
        
        self.entry_branch = self.combo_branchs.get_children()[0]
        
        doc_uri = self.window.get_active_document().get_uri_for_display()
        self.branch_label.set_text(self.githelper.get_branch(doc_uri))   
        
    def close_dialog(self):
        self.dialog.destroy()
        self.dialog = None

    def on_selected(self, *args):
        c = model.get_value(iter, 0)
        self.run_command(c)

    def on_close(self, *args):
        self.close_dialog()

    def on_change(self, *args):
        command = self.entry.get_text()
        description = all_commands_list.get(command, "")
        self.description.set_text(description)

    def on_cancel(self, *args):
        self.close_dialog()

    def on_run(self, *args):
        c = self.entry.get_text()
        self.run_command(c)

    def on_change_branch(self, *args):
        c = self.entry_branch.get_text()
        c = "git checkout %s" % c
        self.run_command(c)

    def deactivate(self, window):
        console = window.get_data("GitHotcommandsPluginInfo")
        bottom = window.get_bottom_panel()
        bottom.remove_item(console)

    def mount_list(self):
        self.model = gtk.ListStore(str)
        for command in all_commands_list.iterkeys():
            self.model.append([command])

    def mount_branchs_list(self):
        doc_uri = self.window.get_active_document().get_uri_for_display()
        branch = self.githelper.get_branch(doc_uri)
        self.model_branchs = gtk.ListStore(str)
        
        for command in self.githelper.get_all_branchs(doc_uri):
            if branch != command:
              self.model_branchs.append([command])
