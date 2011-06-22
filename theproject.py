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
                Repo = git.repo.Repo(repos)
                #print Repo
                #print 'Repo initialised at ', repos
            else:
                Repo = git.repo.Repo(repos,bare=True)
                #print Repo
                #print 'Repo initialised at ', repos
	    new_model = filelist.FileListModel(repos,True)
            self.trvFileSystem.set_model(new_model)
            print repos, 'Selected'
        elif response == gtk.RESPONSE_CANCEL:
            print 'No folder selected, repository not changed'
        dialog.hide()

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
        self.btnPush.show()

        self.btnPull = gtk.Button("Pull")
        self.btnPull.connect("clicked", self.btnPullEvent)
        self.btnPull.show()

        self.btnAdd = gtk.Button("Add")
        self.btnAdd.connect("clicked", self.btnAddEvent)
        self.btnAdd.show()

        self.btnCommit = gtk.Button("Commit")
        self.btnCommit.connect("clicked", self.btnCommitEvent)
        self.btnCommit.show()

        self.btnTrack = gtk.Button("Track")
        self.btnTrack.connect("clicked", self.btnTrackEvent)
        self.btnTrack.show()

        self.btnOpen = gtk.Button("Open")
        self.btnOpen.connect("clicked", self.btnOpenEvent)
        self.btnOpen.show()

        self.btnIgnore = gtk.Button("Ignore")
        self.btnIgnore.connect("clicked", self.btnIgnoreEvent)
        self.btnIgnore.show()

        self.btnBranch = gtk.Button("Branch")
        self.btnBranch.connect("clicked", self.btnBranchEvent)
        self.btnBranch.show()

        self.btnUpload = gtk.Button("Upload")
        self.btnUpload.connect("clicked", self.btnUploadEvent)
        self.btnUpload.show()

        self.btnSwitch = gtk.Button("Switch")
        self.btnSwitch.connect("clicked", self.btnSwitchEvent)
        self.btnSwitch.show()

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

        self.instFileSystemInstance = filelist.FileList(os.path.expanduser('~'))
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

        vbox = gtk.VBox(False, 3)

        table = gtk.Table(4, 4, True)
        table.attach(self.btnPull, 0, 1, 0, 1)
        table.attach(self.btnPush, 1, 2, 0, 1)
        table.attach(self.btnAdd, 2, 3, 0 ,1)
        table.attach(self.btnCommit, 3, 4, 0, 1)
        table.attach(self.btnTrack, 0, 1, 1, 2)
        table.attach(self.btnOpen, 1, 2, 1, 2)
        table.attach(self.btnIgnore, 2, 3, 1, 2)
        table.attach(self.btnBranch, 3, 4, 1, 2)
        table.attach(self.btnUpload, 0, 1, 2, 3)
        table.attach(self.btnSwitch, 1, 2, 2, 3)
        table.show()

        table2 = gtk.Table(1, 2, False)
        table2.attach(self.btnSettings, 0, 1, 0, 1)
        table2.attach(self.txtStatus, 1, 2, 0, 1)
        table2.show()

        vbox.pack_start(self.scrFileListPane, True, True, 0)
        vbox.pack_end(table2, True, False, 0)
        vbox.pack_end(table, True, False, 0)
        vbox.show()

        self.page1 = gtk.Frame()
        self.page1.add(vbox)
        self.page1.show()
        self.notebook.append_page(self.page1)
        self.notebook.set_tab_label_text(self.page1, "Git / FTP")

        self.page2 = gtk.Frame()
        self.page2.add(self.cboInstallPresets)
        self.page2.show()
        self.notebook.append_page(self.page2)
        self.notebook.set_tab_label_text(self.page2, "Auto Installs")

        table3 = gtk.Table(1, 2, False)
        table3.attach(self.btnSettings2, 0, 1, 0, 1)
        table3.attach(self.txtStatus2, 1, 2, 0, 1)
        table3.show()

        vbox3 = gtk.VBox(False, 3)
        vbox3.pack_start(self.lblDownloadLocation, True, False, 0)
        vbox3.pack_start(self.edtDownloadLocation, True, False, 0)
        vbox3.pack_start(self.btnDownload, True, False, 0)
        vbox3.pack_start(self.prgbDownload, True, False, 0)
        vbox3.pack_end(table3, True, False, 0)
        vbox3.show()

        self.page3 = gtk.Frame()
        self.page3.add(vbox3)
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
