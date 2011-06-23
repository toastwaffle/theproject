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
    column_types = (gtk.gdk.Pixbuf, str, str)
    column_names = ['Name', 'Last Changed']

    def __init__(self, dname=None, root=False, rootpath=None):
        gtk.GenericTreeModel.__init__(self)
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
            else:
                return self.filepb
        elif column is 1:
            return rowref
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
        self.listmodel = FileListModel(dirname,True)
 
        # create the TreeView
        self.treeview = gtk.TreeView()
 
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
                new_model = FileListModel(pathname,True)
            else:
                new_model = FileListModel(pathname,False,model.rootpath)
            treeview.set_model(new_model)
            self.globalclass.window.set_title("TheProject - " + os.path.abspath(pathname))
        return
