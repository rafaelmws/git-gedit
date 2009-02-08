import os.path

class GitHelper (object):

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

    def get_branch(self, uri):
        git_root = self.get_git_root(uri)
        return git_root
        #f = open(os.path.join(self.git_root, ".git", "HEAD"))
        #return f.readlines()[0].split("/")[-1]

    def get_all_branchs(self, uri):
        git_root = self.get_git_root(uri)
        diretorios = os.listdir(os.path.join(git_root, ".git", "refs", "heads"))
        return diretorios
