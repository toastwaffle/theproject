#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import os
import sys
sys.path.append(os.getcwd())
import smmap
import async
import gitdb
import git
import filelist
import urllib2

class Base:
    def git_active(self):
        self.btnPull.set_sensitive(True)
        self.btnPush.set_sensitive(True)
        self.btnAdd.set_sensitive(True)
        self.btnCommit.set_sensitive(True)
        self.btnTrack.set_sensitive(True)
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
        
    def destroy(self, widget, data=None):
        gtk.main_quit()

    def btnPushEvent(self, widget):
        print "btnPushEvent entered..."

    def btnPullEvent(self, widget):
        print "btnPullEvent entered..."

    def btnAddEvent(self, widget):
        print "btnAddEvent entered..."

    def btnCommitEvent(self, widget):
        print "btnCommitEvent entered..."

    def btnTrackEvent(self, widget):
        print "btnTrackEvent entered..."

    def btnOpenEvent(self, widget):
        print "btnOpenEvent entered..."

    def btnIgnoreEvent(self, widget):
        print "btnIgnoreEvent entered..."

    def btnBranchEvent(self, widget):
        print "btnBranchEvent entered..."

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
                self.txtStatus.set_text('Using Repo at:\n' + repos)
                self.window.set_title("TheProject - " + repos)
            else:
                dirname = repos + '/.git'
                self.Repo = git.Repo.init(dirname)
                self.txtStatus.set_text('Initialised Repo at:\n' + repos)
                self.window.set_title("TheProject - " + repos)
            new_model = filelist.FileListModel(repos,True)
            self.trvFileSystem.set_model(new_model)
            print repos, 'Selected'
            self.git_active()
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
        dialog = gtk.Dialog("Clone Repo...", self.window, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
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
                self.txtStatus.set_text('Cloned Repo to:\n' + self.edtLocation.get_text())
                self.git_active()
                new_model = filelist.FileListModel(os.path.abspath(self.edtLocation.get_text()),True)
                self.trvFileSystem.set_model(new_model)
            except GitCommandError:
                print 'Couldn\'t Clone Repo, Repo or path invalid'
                self.txtStatus.set_text('Repo or path invalid')
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
        self.txtStatus.set_text('Repo initialised at '+dirname)
        self.git_active()
        new_model = filelist.FileListModel(os.path.abspath(dirname),True)
        self.trvFileSystem.set_model(new_model)

    def btnGitSetupEvent(self, widget):
        print "btnGitSetupEvent entered..."

    def btnFtpSetupEvent(self, widget):
        print "btnFtpSetupEvent entered..."

    def btnSettingsEvent(self, widget):
        print "btnSettingsEvent entered..."

    def btnSettings2Event(self, widget):
        print "btnSettings2Event entered..."

    def btnDownloadEvent(self, widget):
        print "btnDownloadEvent entered..."

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_size_request(350,400)
        self.window.set_title("TheProject")
        self.window.show()
        self.window.connect("destroy", self.destroy)      

        self.notebook = gtk.Notebook()
        self.notebook.set_tab_pos(gtk.POS_TOP)
        self.notebook.show_tabs = True
        self.notebook.show_border = True

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

        self.btnTrack = gtk.Button("Track")
        self.btnTrack.connect("clicked", self.btnTrackEvent)
        self.btnTrack.set_sensitive(False)
        self.btnTrack.show()

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

        self.btnSettings = gtk.Button("Settings")
        self.btnSettings.connect("clicked", self.btnSettingsEvent)
        self.btnSettings.show()

        self.txtStatus = gtk.Label(" { Status/Message Box } ")
        self.txtStatus.show()

        self.btnSettings2 = gtk.Button("Settings")
        self.btnSettings2.connect("clicked", self.btnSettings2Event)
        self.btnSettings2.show()

        self.txtStatus2 = gtk.Label(" { Status/Message Box } ")
        self.txtStatus2.show()

        self.instFileSystemInstance = filelist.FileList(os.path.expanduser('~'),self)
        self.instFileSystemInstance.treeview.columns_autosize()
        self.trvFileSystem = self.instFileSystemInstance.treeview
        self.trvFileSystem.show()

        self.scrFileListPane = gtk.ScrolledWindow()
        self.scrFileListPane.add(self.trvFileSystem)
        self.scrFileListPane.show()

        self.prgbDownload = gtk.ProgressBar(adjustment=None)
        self.prgbDownload.show()

        self.edtDownloadLocation = gtk.Entry()
        self.edtDownloadLocation.show()

        self.lblDownloadLocation = gtk.Label("Download location: ")
        self.lblDownloadLocation.show()

        self.btnDownload = gtk.Button("Download")
        self.btnDownload.connect("clicked", self.btnDownloadEvent)
        self.btnDownload.show()

        self.cboInstallPresets = gtk.ComboBox()
        self.cboInstallPresets.show()

        self.vbox = gtk.VBox(False, 3)

        self.table = gtk.Table(4, 4, True)
        self.table.attach(self.btnPull, 0, 1, 0, 1)
        self.table.attach(self.btnPush, 1, 2, 0, 1)
        self.table.attach(self.btnAdd, 2, 3, 0 ,1)
        self.table.attach(self.btnCommit, 3, 4, 0, 1)
        self.table.attach(self.btnTrack, 0, 1, 1, 2)
        self.table.attach(self.btnUpload, 1, 2, 1, 2)
        self.table.attach(self.btnIgnore, 2, 3, 1, 2)
        self.table.attach(self.btnBranch, 3, 4, 1, 2)
        self.table.attach(self.btnOpen, 0, 1, 2, 3)
        self.table.attach(self.btnSwitch, 1, 2, 2, 3)
        self.table.attach(self.btnClone, 2, 3, 2, 3)
        self.table.attach(self.btnInit, 3, 4, 2, 3)
        self.table.attach(self.btnGitSetup, 0, 2, 3, 4)
        self.table.attach(self.btnFtpSetup, 2, 4, 3, 4)
        self.table.show()

        self.table2 = gtk.Table(1, 2, False)
        self.table2.attach(self.btnSettings, 0, 1, 0, 1)
        self.table2.attach(self.txtStatus, 1, 2, 0, 1)
        self.table2.show()

        self.vbox.pack_start(self.scrFileListPane, True, True, 0)
        self.vbox.pack_end(self.table2, True, False, 0)
        self.vbox.pack_end(self.table, True, False, 0)
        self.vbox.show()

        self.page1 = gtk.Frame()
        self.page1.add(self.vbox)
        self.page1.show()
        self.notebook.append_page(self.page1)
        self.notebook.set_tab_label_text(self.page1, "Git / FTP")

        self.page2 = gtk.Frame()
        self.page2.add(self.cboInstallPresets)
        self.page2.show()
        self.notebook.append_page(self.page2)
        self.notebook.set_tab_label_text(self.page2, "Auto Installs")

        self.table3 = gtk.Table(1, 2, False)
        self.table3.attach(self.btnSettings2, 0, 1, 0, 1)
        self.table3.attach(self.txtStatus2, 1, 2, 0, 1)
        self.table3.show()

        self.vbox3 = gtk.VBox(False, 3)
        self.vbox3.pack_start(self.lblDownloadLocation, True, False, 0)
        self.vbox3.pack_start(self.edtDownloadLocation, True, False, 0)
        self.vbox3.pack_start(self.btnDownload, True, False, 0)
        self.vbox3.pack_start(self.prgbDownload, True, False, 0)
        self.vbox3.pack_end(self.table3, True, False, 0)
        self.vbox3.show()

        self.page3 = gtk.Frame()
        self.page3.add(self.vbox3)
        self.page3.show()
        self.notebook.append_page(self.page3)
        self.notebook.set_tab_label_text(self.page3, "Downloader")

        self.notebook.show()
        self.window.add(self.notebook)

    def main(self):
        gtk.main()

if __name__ == "__main__":
    base = Base()
    base.main()
