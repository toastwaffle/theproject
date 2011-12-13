#!/usr/bin/env python

#Created by toastwaffle && starcube
#github.com/toastwaffle && github.com/starcube

import gobject
import pygtk
pygtk.require('2.0')
import gtk
import os
import sys
sys.path.append(os.getcwd())
import filelist
import smmap
import async
import gitdb
import git
import threading
import webbrowser

class WorkerThread(threading.Thread):
    def __init__(self,function,parent):
        threading.Thread.__init__(self)
        self.function = function
        self.parent = parent
        
    def run(self,*args):
        self.parent.still_working = True
        self.function(*args)
        self.parent.still_working = False
        
    def stop(self):
        self = None

class GitFTP:
    def git_active(self):
        self.gitisactive = True
        self.btnPull.set_sensitive(True)
        self.btnPush.set_sensitive(True)
        self.btnCommit.set_sensitive(True)
        self.btnIgnore.set_sensitive(True)
        self.btnBranch.set_sensitive(True)
        self.btnInit.set_sensitive(False)
        self.btnGitSetup.hide()
        if self.btnFtpSetup.get_visible():
            self.table.remove(self.btnFtpSetup)
            self.table.attach(self.btnFtpSetup, 0, 4, 3, 4)
            
    def ftp_active(self):
        self.btnUpload.set_sensitive(True)
        self.btnFtpSetup.hide()
        if self.btnGitSetup.get_visible:
            self.table.attach(self.btnGitSetup, 0, 4, 3, 4)
   
    def push(self,remoteindex,i):
        if remoteindex == -1:
            for x in self.Repo.remotes:
                x.push()
            with gtk.gdk.lock:
                self.parent.txtStatus.set_text('Pushed repo to all remotes')
            print 'Pushed'
        elif remoteindex >= 0:
            self.Repo.remotes[remoteindex-1].push()
            with gtk.gdk.lock:
                self.parent.txtStatus.set_text('Pushed repo to remote: ' + self.Repo.remotes[remoteindex-1].name)
            print 'Pushed'
        with gtk.gdk.lock:
            self.parent.spnWorking.stop()
            self.parent.spnWorking.hide()
        
    def pull(self,remoteindex,i):
        if remoteindex >= 0:
            self.Repo.remotes[remoteindex].pull()
            with gtk.gdk.lock:
                self.parent.txtStatus.set_text('Pulled repo from remote: ' + self.Repo.remotes[remoteindex].name)
            print 'Pulled'
        with gtk.gdk.lock:
            self.parent.spnWorking.stop()
            self.parent.spnWorking.hide()

    def btnPushEvent(self, widget):
        if len(self.Repo.remotes) != 1:
            cboRemote = gtk.combo_box_new_text()
            cboRemote.append_text("*ALL*")
            for x in self.Repo.remotes:
                cboRemote.append_text(x.name)
            cboRemote.set_active(0)
            cboRemote.show()
            dialog = gtk.Dialog("Select Remote to Push to...", self.parent.window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
            dialog.vbox.pack_start(cboRemote)
            result = dialog.run()
            if result == gtk.RESPONSE_ACCEPT:
                self.parent.spnWorking.show()
                self.parent.spnWorking.start()
                self.parent.txtStatus.set_text('Pushing...')
                WT = WorkerThread(self.push,self)
                WT.start(cboRemote.get_active()-1,0)
            dialog.hide()
        else:
            self.parent.spnWorking.show()
            self.parent.spnWorking.start()
            WT = WorkerThread(self.push,self)
            WT.start(0,0)
        

    def btnPullEvent(self, widget):
        if len(self.Repo.remotes) != 1:
            cboRemote = gtk.combo_box_new_text()
            for x in self.Repo.remotes:
                cboRemote.append_text(x.name)
            cboRemote.set_active(0)
            cboRemote.show()
            dialog = gtk.Dialog("Select Remote to Pull From...", self.parent.window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
            dialog.vbox.pack_start(cboRemote)
            result = dialog.run()
            if result == gtk.RESPONSE_ACCEPT:
                self.parent.spnWorking.show()
                self.parent.spnWorking.start()
                self.parent.txtStatus.set_text('Pulling...')
                WT = WorkerThread(self.pull,self)
                WT.start(cboRemote.get_active(),0)
            dialog.hide()
        else:
            self.parent.spnWorking.show()
            self.parent.spnWorking.start()
            WT = WorkerThread(self.pull,self)
            WT.start(0,0)

    def btnAddEvent(self, widget):
        self.Repo.index.add([self.instFileSystemInstance.gitpath])
        print self.instFileSystemInstance.gitpath, ' added'
        self.parent.txtStatus.set_text(self.instFileSystemInstance.gitpath + ' added')
        self.btnAdd.set_sensitive(False)
        self.btnRemove.set_sensitive(True)

    def btnCommitEvent(self, widget):
        for diff in self.Repo.index.diff(None):
            self.Repo.index.add([diff.a_blob.path])
        edtMessage = gtk.Entry()
        edtMessage.set_text('Commit Message')
        edtMessage.show()
        dialog = gtk.Dialog("Enter Commit Message", self.parent.window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        dialog.vbox.pack_start(edtMessage)
        result = dialog.run()
        if result == gtk.RESPONSE_ACCEPT:
            self.Repo.index.commit(edtMessage.get_text())
            print 'Commited'
        dialog.hide()

    def btnRemoveEvent(self, widget):
        self.Repo.index.remove([self.instFileSystemInstance.gitpath])
        print self.instFileSystemInstance.gitpath, ' removed'
        self.parent.txtStatus.set_text(self.instFileSystemInstance.gitpath + ' removed')
        self.btnAdd.set_sensitive(True)
        self.btnRemove.set_sensitive(False)

    def btnOpenEvent(self, widget):
        webbrowser.open(self.instFileSystemInstance.currpath)

    def btnIgnoreEvent(self, widget):
        path = self.instFileSystemInstance.gitpath
        f = open(repos+"/.gitignore",'a+')
        f.write(path+"\n")
        f.close()
        self.Repo.index.add('.gitignore')

    def btnBranchEvent(self, widget):
        self.tblBranch = gtk.Table(6,3,True)
        self.tblBranch.show()
        self.lblNewBranch = gtk.Label("Name of New Branch")
        self.lblNewBranch.show()
        self.tblBranch.attach(self.lblNewBranch,0,3,0,1)
        self.edtNewBranch = gtk.Entry()
        self.edtNewBranch.show()
        self.tblBranch.attach(self.edtNewBranch,0,3,1,2)
        self.btnNewBranch = gtk.Button("New Branch")
        self.btnNewBranch.show()
        self.btnNewBranch.connect("clicked",self.btnNewBranchEvent)
        self.tblBranch.attach(self.btnNewBranch,0,3,2,3)
        self.cboBranch = gtk.combo_box_new_text()
        for x in self.Repo.branches:
            self.cboBranch.append_text(x.name)
        self.cboBranch.set_active(0)
        self.cboBranch.show()
        self.tblBranch.attach(self.cboBranch,0,3,4,5)
        self.btnCheckout = gtk.Button("Checkout")
        self.btnCheckout.show()
        self.btnCheckout.connect("clicked",self.btnCheckoutEvent)
        self.tblBranch.attach(self.btnCheckout,0,1,5,6)
        self.btnEditBranch = gtk.Button("Edit")
        self.btnEditBranch.show()
        self.btnEditBranch.connect("clicked",self.btnEditBranchEvent)
        self.tblBranch.attach(self.btnEditBranch,1,2,5,6)
        self.btnDeleteBranch = gtk.Button("Delete")
        self.btnDeleteBranch.show()
        self.btnDeleteBranch.connect("clicked",self.btnDeleteBranchEvent)
        self.tblBranch.attach(self.btnDeleteBranch,2,3,5,6)
        dialog = gtk.Dialog("Manage Branches", self.parent.window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        dialog.vbox.pack_start(self.tblBranch)
        dialog.run()
        dialog.hide()
        
    def btnNewBranchEvent(self, widget):
        if self.edtNewBranch.get_text() == "":
            lblError = gtk.Label("Please enter a name.")
            lblError.show()
            errordialog = gtk.Dialog("Error.", self.parent.window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
            errordialog.vbox.pack_start(lblError)
            errordialog.run()
            errordialog.hide()
        try:
            self.Repo.create_head(self.edtNewBranch.get_text())
            self.parent.txtStatus.set_text('Created new branch:\n' + self.edtNewBranch.get_text())
        except OSError:
            lblError = gtk.Label("A branch with that name already exists.\nPlease choose another name.")
            lblError.show()
            errordialog = gtk.Dialog("Error.", self.parent.window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
            errordialog.vbox.pack_start(lblError)
            errordialog.run()
            errordialog.hide()
            
    def btnDeleteBranchEvent(self, widget):
        lblConfirm = gtk.Label("Are you sure you want to delete the branch\n\""+self.Repo.branches[self.cboBranch.get_active()].name+"\"")
        lblConfirm.show()
        confirmdialog = gtk.Dialog("Are you sure?", self.parent.window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        confirmdialog.set_default_response(gtk.RESPONSE_CANCEL)
        confirmdialog.vbox.pack_start(lblConfirm)
        result = confirmdialog.run()
        confirmdialog.hide()
        if result == gtk.RESPONSE_ACCEPT:
            self.Repo.delete_head(self.Repo.branches[self.cboBranch.get_active()])
        
    def btnCheckoutEvent(self, widget):
        try:
            self.Repo.branches[self.cboBranch.get_active()].checkout()
            self.parent.txtStatus.set_text('Checked out branch:\n' + self.Repo.branches[self.cboBranch.get_active()].name)
        except git.GitCommandError:
            lblConfirm = gtk.Label("There are unsaved changes,\ndo you wish to force checkout?")
            lblConfirm.show()
            confirmdialog = gtk.Dialog("Force checkout?", self.parent.window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
            confirmdialog.set_default_response(gtk.RESPONSE_CANCEL)
            confirmdialog.vbox.pack_start(lblConfirm)
            result = confirmdialog.run()
            confirmdialog.hide()
            if result == gtk.RESPONSE_ACCEPT:
                self.Repo.branches[self.cboBranch.get_active()].checkout(True)
                self.parent.txtStatus.set_text('Checked out branch:\n' + self.Repo.branches[self.cboBranch.get_active()].name)
                
    def btnEditBranchEvent(self, widget):
        self.lblEditName = gtk.Label("Name of New Branch")
        self.lblEditName.show()
        self.edtName = gtk.Entry()
        self.edtName.show()
        self.edtName.set_text(self.branches[self.cboBranch.get_active()].name)
        editdialog = gtk.Dialog("Edit Branch", self.parent.window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        editdialog.set_default_response(gtk.RESPONSE_CANCEL)
        editdialog.vbox.pack_start(lblEditName)
        editdialog.vbox.pack_start(edtName)
        result = editdialog.run()
        editdialog.hide()
        if result == gtk.RESPONSE_ACCEPT:
            if self.edtName.get_text() == "":
                lblError = gtk.Label("Please enter a name.")
                lblError.show()
                errordialog = gtk.Dialog("Error.", self.parent.window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
                errordialog.vbox.pack_start(lblError)
                errordialog.run()
                errordialog.hide()
            else:
                self.branches[self.cboBranch.get_active()].rename(self.edtName.get_text())

    def btnUploadEvent(self, widget):
        print "btnUploadEvent entered..."

    def btnSwitchEvent(self, widget):
        dialog = gtk.FileChooserDialog("Select Repo Folder...", None, gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        filter = gtk.FileFilter()
        filter.set_name("All")
        filter.add_pattern("*")
        dialog.add_filter(filter)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            repos = dialog.get_filename()
            if os.path.exists(repos+'/.git'):
                self.Repo = git.repo.Repo(repos)
                self.parent.txtStatus.set_text('Using Repo at:\n' + repos)
                self.parent.window.set_title("TheProject - " + repos)
            else:
                dirname = repos + '/.git'
                self.Repo = git.Repo.init(dirname)
                self.parent.txtStatus.set_text('Initialised Repo at:\n' + repos)
                self.parent.window.set_title("TheProject - " + repos)
            self.git_active()
            new_model = filelist.FileListModel(self,repos,True)
            self.trvFileSystem.set_model(new_model)
            print repos, 'Selected'
        elif response == gtk.RESPONSE_CANCEL:
            print 'No folder selected, repository not changed'
        dialog.hide()

    def btnCloneEvent(self, widget):
        self.edtClone = gtk.Entry()
        self.edtClone.show()
        self.lblClone = gtk.Label("Remote Repo to Clone")
        self.lblClone.show()
        self.edtLocation = gtk.Entry()
        self.edtLocation.set_text(os.path.expanduser("~"))
        self.edtLocation.show()
        self.lblLocation = gtk.Label("Location to Clone to")
        self.lblLocation.show()
        self.btnBrowse = gtk.Button("Browse")
        self.btnBrowse.show()
        self.btnBrowse.connect("clicked",self.btnBrowseEvent)
        dialog = gtk.Dialog("Clone Repo...", self.parent.window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        dialog.vbox.pack_start(self.lblClone)
        dialog.vbox.pack_start(self.edtClone)
        dialog.vbox.pack_end(self.btnBrowse)
        dialog.vbox.pack_end(self.edtLocation)
        dialog.vbox.pack_end(self.lblLocation)
        result = dialog.run()
        if result == gtk.RESPONSE_ACCEPT:
            if not os.path.exists(self.edtLocation.get_text()):
                os.makedirs(self.edtLocation.get_text())
            os.chdir(self.edtLocation.get_text())
            try:
                self.Repo = git.Repo.clone_from(self.edtClone.get_text(),self.edtLocation.get_text())
                dialog.hide()
                print 'Repo Cloned to ',self.edtLocation.get_text()
                self.parent.txtStatus.set_text('Cloned Repo to:\n' + self.edtLocation.get_text())
                self.git_active()
                new_model = filelist.FileListModel(self,os.path.abspath(self.edtLocation.get_text()),True)
                self.trvFileSystem.set_model(new_model)
            except GitCommandError:
                print 'Couldn\'t Clone Repo, Repo or path invalid'
                self.parent.txtStatus.set_text('Repo or path invalid')
                dialog.run()
        else:
            dialog.hide()
        
    def btnBrowseEvent(self, widget):
        dialog = gtk.FileChooserDialog("Select Folder to clone to...", None, gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        filter = gtk.FileFilter()
        filter.set_name("All")
        filter.add_pattern("*")
        dialog.add_filter(filter)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            self.edtLocation.set_text(dialog.get_filename())
            print 'Location changed to ', dialog.get_filename()
        elif response == gtk.RESPONSE_CANCEL:
            print 'No folder selected, location not changed'
        dialog.hide()

    def btnInitEvent(self, widget):
        model = self.trvFileSystem.get_model()
        dirname = model.dirname
        self.Repo = git.Repo.init(dirname)
        print 'Git Repo initialised at', dirname
        self.parent.txtStatus.set_text('Repo initialised at '+dirname)
        self.git_active()
        new_model = filelist.FileListModel(self,os.path.abspath(dirname),True)
        self.trvFileSystem.set_model(new_model)

    def btnGitSetupEvent(self, widget):
        print "btnGitSetupEvent entered..."

    def btnFtpSetupEvent(self, widget):
        print "btnFtpSetupEvent entered..."

    def __init__(self,parent):
    
        self.parent = parent
        self.gitisactive = False
        self.ftpisactive = False
        
        self.btnPush = gtk.Button("Push")
        self.btnPush.connect("clicked", self.btnPushEvent)
        self.btnPush.set_sensitive(False)
        self.btnPush.show()

        self.btnPull = gtk.Button("Pull")
        self.btnPull.connect("clicked", self.btnPullEvent)
        self.btnPull.set_sensitive(False)
        self.btnPull.show()

        self.btnAdd = gtk.Button("Add")
        self.btnAdd.connect("clicked", self.btnAddEvent)
        self.btnAdd.set_sensitive(False)
        self.btnAdd.show()

        self.btnCommit = gtk.Button("Commit")
        self.btnCommit.connect("clicked", self.btnCommitEvent)
        self.btnCommit.set_sensitive(False)
        self.btnCommit.show()

        self.btnRemove = gtk.Button("Remove")
        self.btnRemove.connect("clicked", self.btnRemoveEvent)
        self.btnRemove.set_sensitive(False)
        self.btnRemove.show()

        self.btnOpen = gtk.Button("Open")
        self.btnOpen.connect("clicked", self.btnOpenEvent)
        self.btnOpen.show()

        self.btnIgnore = gtk.Button("Ignore")
        self.btnIgnore.connect("clicked", self.btnIgnoreEvent)
        self.btnIgnore.set_sensitive(False)
        self.btnIgnore.show()

        self.btnBranch = gtk.Button("Branch")
        self.btnBranch.connect("clicked", self.btnBranchEvent)
        self.btnBranch.set_sensitive(False)
        self.btnBranch.show()

        self.btnUpload = gtk.Button("Upload")
        self.btnUpload.connect("clicked", self.btnUploadEvent)
        self.btnUpload.set_sensitive(False)
        self.btnUpload.show()

        self.btnSwitch = gtk.Button("Switch")
        self.btnSwitch.connect("clicked", self.btnSwitchEvent)
        self.btnSwitch.show()

        self.btnClone = gtk.Button("Clone")
        self.btnClone.connect("clicked", self.btnCloneEvent)
        self.btnClone.show()

        self.btnGitSetup = gtk.Button("Setup Git")
        self.btnGitSetup.connect("clicked", self.btnGitSetupEvent)
        self.btnGitSetup.show()

        self.btnFtpSetup = gtk.Button("Setup FTP")
        self.btnFtpSetup.connect("clicked", self.btnFtpSetupEvent)
        self.btnFtpSetup.show()

        self.btnInit = gtk.Button("Init")
        self.btnInit.connect("clicked", self.btnInitEvent)
        self.btnInit.show()

        self.instFileSystemInstance = filelist.FileList(os.path.expanduser('~'),self)
        self.instFileSystemInstance.treeview.columns_autosize()
        self.trvFileSystem = self.instFileSystemInstance.treeview
        self.trvFileSystem.show()

        self.scrFileListPane = gtk.ScrolledWindow()
        self.scrFileListPane.add(self.trvFileSystem)
        self.scrFileListPane.show()
        
        self.table = gtk.Table(4, 4, True)
        self.table.attach(self.btnPull, 0, 1, 0, 1)
        self.table.attach(self.btnPush, 1, 2, 0, 1)
        self.table.attach(self.btnAdd, 2, 3, 0 ,1)
        self.table.attach(self.btnIgnore, 3, 4, 0, 1)
        self.table.attach(self.btnCommit, 0, 1, 1, 2)
        self.table.attach(self.btnUpload, 1, 2, 1, 2)
        self.table.attach(self.btnRemove, 2, 3, 1, 2)
        self.table.attach(self.btnBranch, 3, 4, 1, 2)
        self.table.attach(self.btnOpen, 0, 1, 2, 3)
        self.table.attach(self.btnSwitch, 1, 2, 2, 3)
        self.table.attach(self.btnClone, 2, 3, 2, 3)
        self.table.attach(self.btnInit, 3, 4, 2, 3)
        self.table.attach(self.btnGitSetup, 0, 2, 3, 4)
        self.table.attach(self.btnFtpSetup, 2, 4, 3, 4)
        self.table.show()

        self.vbox = gtk.VBox(False, 3)        
        self.vbox.pack_start(self.scrFileListPane, True, True, 0)
        self.vbox.pack_end(self.table, False, False, 0)
        self.vbox.show()
        
        self.page = gtk.Frame()
        self.page.add(self.vbox)
        self.page.show()
