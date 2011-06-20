#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

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
        print "btnSwitchEvent entered..."

    def btnSettingsEvent(self, widget):
        print "btnSettingsEvent entered..."

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_size_request(350,400)
        self.window.set_title("TheProject")
        self.window.show()
        self.window.connect("destroy", self.destroy)      

        notebook = gtk.Notebook()
        notebook.set_tab_pos(gtk.POS_TOP)
        notebook.show_tabs = True
        notebook.show_border = True

        """dialog = gtk.FileChooserDialog("Open...", None, gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        filter = gtk.FileFilter()
        filter.set_name("All Files")
        filter.add_pattern("*")
        dialog.add_filter(filter)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            print dialog.get_filename(), 'Selected'
        elif response == gtk.RESPONSE_CANCEL:
            print 'You didnt choose any files!'
        dialog.hide()"""

        btnPush = gtk.Button("Push")
        btnPush.connect("clicked", self.btnPushEvent)
        btnPush.show()

        btnPull = gtk.Button("Pull")
        btnPull.connect("clicked", self.btnPullEvent)
        btnPull.show()

        btnAdd = gtk.Button("Add")
        btnAdd.connect("clicked", self.btnAddEvent)
        btnAdd.show()

        btnCommit = gtk.Button("Commit")
        btnCommit.connect("clicked", self.btnCommitEvent)
        btnCommit.show()

        btnTrack = gtk.Button("Track")
        btnTrack.connect("clicked", self.btnTrackEvent)
        btnTrack.show()

        btnOpen = gtk.Button("Open")
        btnOpen.connect("clicked", self.btnOpenEvent)
        btnOpen.show()

        btnIgnore = gtk.Button("Ignore")
        btnIgnore.connect("clicked", self.btnIgnoreEvent)
        btnIgnore.show()

        btnBranch = gtk.Button("Branch...")
        btnBranch.connect("clicked", self.btnBranchEvent)
        btnBranch.show()

        btnUpload = gtk.Button("Upload")
        btnUpload.connect("clicked", self.btnUploadEvent)
        btnUpload.show()

        btnSwitch = gtk.Button("Switch...")
        btnSwitch.connect("clicked", self.btnSwitchEvent)
        btnSwitch.show()

        btnSettings = gtk.Button("Settings")
        btnSettings.connect("clicked", self.btnSettingsEvent)
        btnSettings.show()

        txtStatus = gtk.Entry()
        txtStatus.show()

        fixedLayout = gtk.Fixed()
        fixedLayout.put(btnPush, 0, 250)
        fixedLayout.put(btnPull, 0, 280)
        fixedLayout.put(btnAdd, 0, 310)
        fixedLayout.put(btnCommit, 20, 0)
        fixedLayout.put(btnTrack, 20, 30)
        fixedLayout.put(btnOpen, 20, 60)
        fixedLayout.put(btnIgnore, 20, 90)
        fixedLayout.put(btnBranch, 20, 110)
        fixedLayout.put(btnUpload, 20, 200)
        fixedLayout.put(btnSwitch, 50, 0)
        fixedLayout.put(btnSettings, 100, 0)
        fixedLayout.put(txtStatus, 100, 25)

        fixedLayout.show()

        page1 = gtk.Frame()
        page1.add(fixedLayout)
        page1.show()
        notebook.append_page(page1)
        notebook.set_tab_label_text(page1, "Git / FTP")

        page2 = gtk.Label("This is gonna be replaced by content...\n...Soon...\n...Hopefully...;)")
        page2.show()
        notebook.append_page(page2)
        notebook.set_tab_label_text(page2, "Auto Installs")

        page3 = gtk.Label("This is gonna be replaced by content...\n...Soon...\n...Hopefully...;)")
        page3.show()
        notebook.append_page(page3)
        notebook.set_tab_label_text(page3, "Downloader")

        notebook.show()
        self.window.add(notebook)

    def main(self):
        gtk.main()

if __name__ == "__main__":
    base = Base()
    base.main()
