import os, stat, time
import pygtk
pygtk.require('2.0')
import gtk

class FileListModel(gtk.GenericTreeModel):
    folderxpm = [
        "17 16 7 1",
        "  c #000000",
        ". c #808000",
        "X c yellow",
        "o c #808080",
        "O c #c0c0c0",
        "+ c white",
        "@ c None",
        "@@@@@@@@@@@@@@@@@",
        "@@@@@@@@@@@@@@@@@",
        "@@+XXXX.@@@@@@@@@",
        "@+OOOOOO.@@@@@@@@",
        "@+OXOXOXOXOXOXO. ",
        "@+XOXOXOXOXOXOX. ",
        "@+OXOXOXOXOXOXO. ",
        "@+XOXOXOXOXOXOX. ",
        "@+OXOXOXOXOXOXO. ",
        "@+XOXOXOXOXOXOX. ",
        "@+OXOXOXOXOXOXO. ",
        "@+XOXOXOXOXOXOX. ",
        "@+OOOOOOOOOOOOO. ",
        "@                ",
        "@@@@@@@@@@@@@@@@@",
        "@@@@@@@@@@@@@@@@@"
    ]
    folderpb = gtk.gdk.pixbuf_new_from_xpm_data(folderxpm)

    filexpm = [
        "12 12 3 1",
        "  c #000000",
        ". c #ffff04",
        "X c #b2c0dc",
        "X        XXX",
        "X ...... XXX",
        "X ......   X",
        "X .    ... X",
        "X ........ X",
        "X .   .... X",
        "X ........ X",
        "X .     .. X",
        "X ........ X",
        "X .     .. X",
        "X ........ X",
        "X          X"
    ]
    filepb = gtk.gdk.pixbuf_new_from_xpm_data(filexpm)

    newxpm = [
        "12 12 5 1",
        "  c #000000",
        ". c #ffff04",
        "X c #b2c0dc",
        "g c green",
        "w c white",
        "X     gg  gg",
        "X ....gg  gg",
        "X ....      ",
        "X .  .      ",
        "X ....gg  gg",
        "X .   gg  gg",
        "X ........ X",
        "X .     .. X",
        "X ........ X",
        "X .     .. X",
        "X ........ X",
        "X          X"
    ]
    newpb = gtk.gdk.pixbuf_new_from_xpm_data(newxpm)

    renamedxpm = [
        "12 12 4 1",
        "  c #000000",
        ". c #ffff04",
        "X c #b2c0dc",
        "o c #ff6600",
        "X     oooooo",
        "X ....oooooo",
        "X ....oooooo",
        "X .   oooooo",
        "X ....oooooo",
        "X .   oooooo",
        "X ........ X",
        "X .     .. X",
        "X ........ X",
        "X .     .. X",
        "X ........ X",
        "X          X"
    ]
    renamedpb = gtk.gdk.pixbuf_new_from_xpm_data(renamedxpm)

    changedxpm = [
        "12 12 5 1",
        "  c #000000",
        ". c #ffff04",
        "X c #b2c0dc",
        "g c #00ff00",
        "h c #33ff00",
        "X     ghghgh",
        "X ....hghghg",
        "X ....ghghgh",
        "X .   hghghg",
        "X ....ghghgh",
        "X .   hghghg",
        "X ........ X",
        "X .     .. X",
        "X ........ X",
        "X .     .. X",
        "X ........ X",
        "X          X"
    ]
    changedpb = gtk.gdk.pixbuf_new_from_xpm_data(changedxpm)
    column_types = (gtk.gdk.Pixbuf, str, str, str)
    column_names = ['Name', 'Status', 'Last Changed']

    def __init__(self,globalclass, dname=None, root=False, rootpath=None):
        gtk.GenericTreeModel.__init__(self)
        self.globalclass = globalclass
        self.changed = []
        self.renamed = []
        self.newfiles = []
        if self.globalclass.gitisactive:
            for x in globalclass.Repo.index.diff(None):
                fullpath = globalclass.Repo.working_dir+"/"+x.a_blob.path
                if x.renamed:
                    fullpath = globalclass.Repo.working_dir+"/"+x.renamed_to
                    self.renamed.append(fullpath)
                elif x.new_file:
                    self.newfiles.append(fullpath)
                else:
                    self.changed.append(fullpath)
            for x in globalclass.Repo.untracked_files:
                fullpath = globalclass.Repo.working_dir+"/"+x
                self.newfiles.append(fullpath)
        if not dname:
            self.dirname = os.path.expanduser('~')
        else:
            self.dirname = os.path.abspath(dname)
        self.dirsfiles = [f for f in os.listdir(self.dirname) if f[0] <> '.']
        self.dirsfiles.sort(key=str.lower)
        self.files = []
        self.dirs = []
        for x in self.dirsfiles:
            fname = os.path.join(self.dirname, x)
            try:
                filestat = os.stat(fname)
            except OSError:
                return None
            mode = filestat.st_mode
            if stat.S_ISDIR(mode):
                self.dirs.append(x)
            else:
                self.files.append(x)
        if root:
            self.files = self.dirs + self.files
            self.rootpath = self.dirname
	else:
            self.files = ['..'] + self.dirs + self.files
            self.rootpath = rootpath
        return

    def get_pathname(self, path):
        filename = self.files[path[0]]
        return os.path.join(self.dirname, filename)

    def is_folder(self, path):
        filename = self.files[path[0]]
        pathname = os.path.join(self.dirname, filename)
        filestat = os.stat(pathname)
        if stat.S_ISDIR(filestat.st_mode):
            return True
        return False

    def get_column_names(self):
        return self.column_names[:]

    def on_get_flags(self):
        return gtk.TREE_MODEL_LIST_ONLY|gtk.TREE_MODEL_ITERS_PERSIST

    def on_get_n_columns(self):
        return len(self.column_types)

    def on_get_column_type(self, n):
        return self.column_types[n]

    def on_get_iter(self, path):
        return self.files[path[0]]

    def on_get_path(self, rowref):
        return self.files.index(rowref)

    def on_get_value(self, rowref, column):
        fname = os.path.join(self.dirname, rowref)
        try:
            filestat = os.stat(fname)
        except OSError:
            return None
        mode = filestat.st_mode
        if column is 0:
            if stat.S_ISDIR(mode):
                return self.folderpb
            elif fname in self.changed:
                return self.changedpb
            elif fname in self.newfiles:
                return self.newpb
            elif fname in self.renamed:
                return self.renamedpb
            else:
                return self.filepb
        elif column is 1:
            return rowref
        elif column is 2:
            if stat.S_ISDIR(mode):
                return ""
            elif fname in self.changed:
                return "File Has Changed"
            elif fname in self.newfiles:
                return "New File"
            elif fname in self.renamed:
                return "Renamed"
            else:
                return "Unchanged"
        return time.ctime(filestat.st_mtime)

    def on_iter_next(self, rowref):
        try:
            i = self.files.index(rowref)+1
            return self.files[i]
        except IndexError:
            return None

    def on_iter_children(self, rowref):
        if rowref:
            return None
        return self.files[0]

    def on_iter_has_child(self, rowref):
        return False

    def on_iter_n_children(self, rowref):
        if rowref:
            return 0
        return len(self.files)

    def on_iter_nth_child(self, rowref, n):
        if rowref:
            return None
        try:
            return self.files[n]
        except IndexError:
            return None

    def on_iter_parent(child):
        return None

class FileList:
    def __init__(self,dirname,globalclass):
        self.globalclass = globalclass
        self.listmodel = FileListModel(globalclass,dirname,True,None)
 
        # create the TreeView
        self.treeview = gtk.TreeView()

        treeselection = self.treeview.get_selection()
        treeselection.set_mode(gtk.SELECTION_SINGLE)
        # create the TreeViewColumns to display the data
        column_names = self.listmodel.get_column_names()
        self.tvcolumn = [None] * len(column_names)
        cellpb = gtk.CellRendererPixbuf()
        self.tvcolumn[0] = gtk.TreeViewColumn(column_names[0],
                                              cellpb, pixbuf=0)
        cell = gtk.CellRendererText()
        self.tvcolumn[0].pack_start(cell, False)
        self.tvcolumn[0].add_attribute(cell, 'text', 1)
        self.treeview.append_column(self.tvcolumn[0])
        for n in range(1, len(column_names)):
            cell = gtk.CellRendererText()
            if n == 1:
                cell.set_property('xalign', 1.0)
            self.tvcolumn[n] = gtk.TreeViewColumn(column_names[n],
                                                  cell, text=n+1)
            self.treeview.append_column(self.tvcolumn[n])

        self.treeview.connect('row-activated', self.open_file)
        self.treeview.connect('cursor-changed', self.change_cursor)
        self.treeview.set_model(self.listmodel)
        return

    def open_file(self, treeview, path, column):
        model = treeview.get_model()
        if model.is_folder(path):
            pathname = model.get_pathname(path)
            if os.path.exists(pathname+'/.git'):
                self.globalclass.btnInit.set_sensitive(False)
            else:
                self.globalclass.btnInit.set_sensitive(True)                
            if os.path.abspath(pathname) == os.path.abspath(model.rootpath):
                new_model = FileListModel(self.globalclass,pathname,True,None)
            else:
                new_model = FileListModel(self.globalclass,pathname,False,model.rootpath)
            treeview.set_model(new_model)
            self.globalclass.window.set_title("TheProject - " + os.path.abspath(pathname))
        return
   
    def change_cursor(self, treeview):
        model = treeview.get_model()
        self.currpath =  model.get_pathname(treeview.get_cursor()[0])
        print self.currpath
        if self.globalclass.gitisactive:
            workdir = self.globalclass.Repo.working_dir + '/'
            self.gitpath = self.currpath.replace(workdir,'')
            filestat = os.stat(self.currpath)
            if stat.S_ISDIR(filestat.st_mode):
                self.globalclass.btnAdd.set_sensitive(False)
                self.globalclass.btnRemove.set_sensitive(False)
            else:
                print self.gitpath
                if self.globalclass.Repo.index.entries.has_key((self.gitpath, 0)):
                    self.globalclass.btnAdd.set_sensitive(False)
                    self.globalclass.btnRemove.set_sensitive(True)
                else:
                    self.globalclass.btnAdd.set_sensitive(True)
                    self.globalclass.btnRemove.set_sensitive(False)
        return
